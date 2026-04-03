import asyncio
import json
import logging
from typing import Any, Dict, Optional

from aiohttp import ClientSession
from aiohttp.client import DEFAULT_TIMEOUT
from aiohttp.client_exceptions import ClientResponseError

logger = logging.getLogger(__name__)

class BoostcampEndpoints(object):
    BASE_URL = "https://newapi.boostcamp.app/api/www"

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

class BoostcampAPI(object):
    def __init__(
        self,
        token: Optional[str] = None,
        timeout: int = 10,
    ) -> None:
        self._token = token
        self._timeout = timeout
        
        self._headers = {
            "Accept": "*/*",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": "https://www.boostcamp.app",
            "Referer": "https://www.boostcamp.app/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }
        if token:
            self._headers["Authorization"] = f"FirebaseIdToken:{self.token}"

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
        self._headers["Authorization"] = f"FirebaseIdToken:{self.token}"

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
