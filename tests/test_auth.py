import pickle

from boostcampapi.boostcampapi import BoostcampAPI, BoostcampEndpoints


async def test_login_captures_refresh_token(fake_http):
    """login() should keep the refreshToken from the Firebase response, not just the idToken."""
    fake_http.register(
        BoostcampEndpoints.FIREBASE_LOGIN_URL,
        json={"idToken": "tok1", "refreshToken": "refresh1", "expiresIn": "3600"},
    )
    api = BoostcampAPI()
    await api.login("user@example.com", "hunter2", save_session=False)

    assert api.token == "tok1"
    assert api._refresh_token == "refresh1"


async def test_save_session_does_not_persist_password(fake_http, tmp_path):
    """The pickled session must contain the refresh token but never the plaintext password."""
    fake_http.register(
        BoostcampEndpoints.FIREBASE_LOGIN_URL,
        json={"idToken": "tok1", "refreshToken": "refresh1", "expiresIn": "3600"},
    )
    session_file = tmp_path / "session.pickle"
    api = BoostcampAPI(session_file=str(session_file))
    await api.login("user@example.com", "hunter2")

    with open(session_file, "rb") as fh:
        stored = pickle.load(fh)

    assert stored["token"] == "tok1"
    assert stored["refresh_token"] == "refresh1"
    assert "password" not in stored
    assert "hunter2" not in stored.values()


def test_load_session_restores_refresh_token(tmp_path):
    """load_session() should restore the token and refresh token from a saved session."""
    session_file = tmp_path / "session.pickle"
    with open(session_file, "wb") as fh:
        pickle.dump({"token": "tokA", "refresh_token": "refreshA"}, fh)

    api = BoostcampAPI(session_file=str(session_file))
    assert api.load_session() is True
    assert api.token == "tokA"
    assert api._refresh_token == "refreshA"


async def test_refresh_session_exchanges_refresh_token(fake_http):
    """_refresh_session() should POST a refresh_token grant and adopt the new tokens."""
    fake_http.register(
        BoostcampEndpoints.FIREBASE_REFRESH_URL,
        json={"id_token": "tok2", "refresh_token": "refresh2", "expires_in": "3600"},
    )
    api = BoostcampAPI(token="tok1")
    api._refresh_token = "refresh1"

    assert await api._refresh_session() is True
    assert api.token == "tok2"
    assert api._refresh_token == "refresh2"

    call = fake_http.calls[-1]
    assert call.url == BoostcampEndpoints.FIREBASE_REFRESH_URL
    sent = call.data or call.json
    assert sent["grant_type"] == "refresh_token"
    assert sent["refresh_token"] == "refresh1"


async def test_refresh_session_returns_false_without_refresh_token(fake_http):
    """_refresh_session() should be a no-op (return False) when no refresh token is held."""
    api = BoostcampAPI(token="tok1")
    assert await api._refresh_session() is False
    assert fake_http.calls == []


async def test_post_refreshes_token_on_403_and_retries(fake_http):
    """A 403 should trigger a refresh-token exchange and a retry with the new token."""
    endpoint = BoostcampEndpoints.get_user_endpoint()
    fake_http.register(endpoint, status=403)
    fake_http.register(
        BoostcampEndpoints.FIREBASE_REFRESH_URL,
        json={"id_token": "tok2", "refresh_token": "refresh2", "expires_in": "3600"},
    )
    fake_http.register(endpoint, status=200, json={"user": "me"})

    api = BoostcampAPI(token="tok1")
    api._refresh_token = "refresh1"
    result = await api.get_user_profile()

    assert result == {"user": "me"}
    assert api.token == "tok2"
    retry_call = fake_http.calls[-1]
    assert retry_call.url == endpoint
    assert retry_call.headers["Authorization"] == "FirebaseIdToken:tok2"
