"""Test helpers: a version-independent fake ``aiohttp.ClientSession``.

aioresponses pins to aiohttp internals that drift between releases, so instead
we patch the ``ClientSession`` symbol used by the client with a small fake that
exercises the real request/response code paths (payload construction, status
handling, token updates) without touching the network.
"""
from collections import defaultdict, deque
from types import SimpleNamespace

import pytest
from aiohttp.client_exceptions import ClientResponseError

import boostcampapi.boostcampapi as boostcampapi


class _FakeResponse:
    def __init__(self, status, json_data=None, text_data=""):
        self.status = status
        self._json = json_data
        self._text = text_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def json(self):
        return self._json

    async def text(self):
        return self._text

    def raise_for_status(self):
        if self.status >= 400:
            raise ClientResponseError(
                request_info=SimpleNamespace(real_url="http://test"),
                history=(),
                status=self.status,
                message=f"HTTP {self.status}",
            )


class FakeHTTP:
    """Registers queued responses per URL and records the calls made."""

    def __init__(self):
        self._responses = defaultdict(deque)
        self.calls = []

    def register(self, url, status=200, json=None, text=""):
        self._responses[url].append(_FakeResponse(status, json, text))

    def _session_factory(fake_http):
        class _FakeSession:
            def __init__(self, *args, headers=None, **kwargs):
                self._headers = dict(headers) if headers else {}

            async def __aenter__(self):
                return self

            async def __aexit__(self, *exc):
                return False

            def post(self, url, json=None, data=None, timeout=None):
                fake_http.calls.append(
                    SimpleNamespace(
                        url=url, json=json, data=data, headers=self._headers
                    )
                )
                queue = fake_http._responses.get(url)
                if not queue:
                    raise AssertionError(f"No fake response registered for {url}")
                return queue.popleft()

        return _FakeSession


@pytest.fixture
def fake_http(monkeypatch):
    fake = FakeHTTP()
    monkeypatch.setattr(boostcampapi, "ClientSession", fake._session_factory())
    return fake
