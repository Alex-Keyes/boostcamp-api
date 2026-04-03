import asyncio
import json
import logging
import os
import pickle
from typing import Any, Dict, Optional

from aiohttp import ClientSession
from aiohttp.client import DEFAULT_TIMEOUT
from aiohttp.client_exceptions import ClientResponseError

logger = logging.getLogger(__name__)

SESSION_DIR = ".boostcamp"
SESSION_FILE = f"{SESSION_DIR}/session.pickle"

class BoostcampEndpoints(object):
    BASE_URL = "https://newapi.boostcamp.app/api/www"
    FIREBASE_API_KEY = "AIzaSyAEJcoGF-5ueF3bvaujcJm2PUV7RHKQwTw"
    FIREBASE_LOGIN_URL = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_API_KEY}"
    FIREBASE_RESET_URL = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={FIREBASE_API_KEY}"

    @classmethod
    def get_user_endpoint(cls) -> str:
        return cls.BASE_URL + "/users/get"

    @classmethod
    def get_programs_endpoint(cls) -> str:
        return cls.BASE_URL + "/user_programs/list"

    @classmethod
    def create_exercise_endpoint(cls) -> str:
        return cls.BASE_URL + "/user_exercise/create"

class BoostcampAuthException(Exception):
    pass

class RequestFailedException(Exception):
    pass

class LoginFailedException(Exception):
    pass

class BoostcampAPI(object):
    def __init__(
        self,
        token: Optional[str] = None,
        timeout: int = 10,
        session_file: str = SESSION_FILE,
    ) -> None:
        self._token = token
        self._timeout = timeout
        self._session_file = session_file
        
        self._headers = {
            "Accept": "*/*",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": "https://www.boostcamp.app",
            "Referer": "https://www.boostcamp.app/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }
        if token:
            self._headers["Authorization"] = f"FirebaseIdToken:{self._token}"

    @property
    def timeout(self) -> int:
        return self._timeout

    def set_timeout(self, timeout_secs: int) -> None:
        self._timeout = timeout_secs

    @property
    def token(self) -> Optional[str]:
        return self._token

    def set_token(self, token: str) -> None:
        self._token = token
        self._headers["Authorization"] = f"FirebaseIdToken:{self._token}"

    async def login(
        self,
        email: str,
        password: str,
        save_session: bool = True,
    ) -> None:
        """Logs into Boostcamp using Firebase Identity Toolkit."""
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        async with ClientSession() as session:
            try:
                async with session.post(
                    BoostcampEndpoints.FIREBASE_LOGIN_URL,
                    json=payload,
                    timeout=self._timeout
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise LoginFailedException(f"Login failed ({response.status}): {error_text}")
                    
                    data = await response.json()
                    self.set_token(data["idToken"])
                    
                    if save_session:
                        self.save_session()
            except Exception as e:
                if isinstance(e, LoginFailedException):
                    raise
                raise LoginFailedException(f"An error occurred during login: {str(e)}") from e

    async def request_password_reset(self, email: str) -> Dict[str, Any]:
        """Triggers a Firebase password reset email. Useful for OAuth users setting a password for the first time."""
        payload = {
            "requestType": "PASSWORD_RESET",
            "email": email
        }
        async with ClientSession() as session:
            async with session.post(BoostcampEndpoints.FIREBASE_RESET_URL, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise RequestFailedException(f"Reset request failed ({response.status}): {error_text}")
                return await response.json()

    def save_session(self, filename: Optional[str] = None) -> None:
        """Saves the auth token to a pickle file."""
        if filename is None:
            filename = self._session_file
        filename = os.path.abspath(filename)
        
        session_data = {"token": self._token}
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as fh:
            pickle.dump(session_data, fh)

    def load_session(self, filename: Optional[str] = None) -> bool:
        """Loads auth token from a pickle file."""
        if filename is None:
            filename = self._session_file
        
        if not os.path.exists(filename):
            return False
            
        with open(filename, "rb") as fh:
            data = pickle.load(fh)
            self.set_token(data["token"])
            return True

    async def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Performs a POST request to a given endpoint."""
        if data is None:
            data = {}
            
        async with ClientSession(headers=self._headers) as session:
            try:
                async with session.post(
                    endpoint,
                    json=data,
                    timeout=self._timeout
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except ClientResponseError as e:
                if e.status == 403:
                    raise BoostcampAuthException(f"Auth error (403): Your FirebaseIdToken may have expired.") from e
                raise RequestFailedException(f"Request failed: {e.status} {e.message}") from e
            except Exception as e:
                raise RequestFailedException(f"An unexpected error occurred: {str(e)}") from e

    async def get_user_profile(self) -> Dict[str, Any]:
        """Returns the logged-in user's profile and settings."""
        return await self._post(BoostcampEndpoints.get_user_endpoint())

    async def list_user_programs(self) -> Dict[str, Any]:
        """Returns the list of programs the user is enrolled in."""
        return await self._post(BoostcampEndpoints.get_programs_endpoint())
