import random
import httpx
from typing import Optional, Dict, Any
import time
from returns.result import Result, Success, Failure

from src.config import Config
from src.errors import (
    Error,
    NetworkError,
    HTTPError,
    TimeoutError,
    NotFoundError,
    RateLimitError,
)


# docs = https://www.python-httpx.org/
class APIClient:
    """Basic HTTP Client"""

    def __init__(self, base_url: str):
        self.base_url: str = base_url

        self.timeout: httpx.Timeout = httpx.Timeout(
            connect=Config.API_CONNECT_TIMEOUT,
            read=Config.API_READ_TIMEOUT,
            write=Config.API_WRITE_TIMEOUT,
            pool=Config.API_POOL_TIMEOUT
        )
        self.ttl: int = Config.CACHE_TTL_TIME
        self.max_retry: int = Config.MAX_RETRIES

        self.enable_retry: bool = Config.ENABLE_RETRY
        self.enable_cache: bool = Config.ENABLE_CACHE

        self._cache: Dict[str, tuple] = {}

        self.client = httpx.Client(timeout=self.timeout)

    def _get_from_cache(self, key: str) -> Optional[Any]:
        if not self.enable_cache:
            return None

        entry = self._cache.get(key)
        if not entry:
            return None

        data, timestamp = entry
        if time.time() - timestamp < self.ttl:
            return data

        return None

    def _save_to_cache(self, key: str, data: Any) -> None:
        if self.enable_cache:
            self._cache[key] = (data, time.time())

    def get(self, endpoint: str) -> Result[Dict[Any, Any], Error]:
        """GET with TTL cache"""
        url = f"{self.base_url}{endpoint}"

        cached = self._get_from_cache(url)
        if cached is not None:
            return Success(cached)

        last_error: Error = NetworkError()

        for attempts in range(self.max_retry + 1):
            retryable = False
            try:
                response = self.client.get(url)
                response.raise_for_status()

                try:
                    data = response.json()
                except ValueError:
                    data = response.text

                self._save_to_cache(url, data)
                return Success(data)

            except httpx.HTTPStatusError as e:
                status = e.response.status_code
                retryable = 500 <= status < 600
                if status == 404:
                    last_error = NotFoundError(details=str(e))
                elif status == 429:
                    retry_after = e.response.headers.get("Retry-After")
                    last_error = RateLimitError(retry_after=int(retry_after) if retry_after else None, details=str(e))
                else:
                    last_error = HTTPError(status_code=status, details=str(e))
            except httpx.TimeoutException as e:
                retryable = True
                last_error = TimeoutError(details=str(e))
            except httpx.NetworkError as e:
                retryable = True
                last_error = NetworkError(details=str(e))

            if not self.enable_retry or not retryable or attempts >= self.max_retry:
                return Failure(last_error)

            sleep_time = min(10, random.randint(0, 2**attempts)) # Exponential Backoff with Full Jitter
            time.sleep(sleep_time)

        return Failure(last_error)
