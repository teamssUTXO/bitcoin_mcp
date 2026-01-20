import httpx
from typing import Optional, Dict, Any
import time

from src.config import Config

class APIClient:
    """Client HTTP de base avec retry, timeout et cache"""
    
    def __init__(self, base_url: str):
        self.base_url: str = base_url

        self.timeout: int = Config.API_TIMEOUT
        self.ttl: int = Config.CACHE_TTL_TIME
        self._cache: Dict[str, tuple] = {}
    
    def get(self, endpoint: str) -> Optional[Dict[Any, Any]]:
        """GET avec cache TTL"""
        cache_key = f"{self.base_url}{endpoint}"
        
        if cache_key in self._cache:
            data, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self.ttl:
                return data
        
        try:
            response = httpx.get(
                f"{self.base_url}{endpoint}",
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            self._cache[cache_key] = (data, time.time())
            return data
        except Exception:
            return None