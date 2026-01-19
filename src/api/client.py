import httpx
from typing import Optional, Dict, Any
from functools import lru_cache
import time

class APIClient:
    """Client HTTP de base avec retry, timeout et cache"""
    
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url: str = base_url

        self.timeout: int = timeout
        self._cache: Dict[str, tuple] = {}
    
    def get(self, endpoint: str, ttl: int = 60) -> Optional[Dict[Any, Any]]:
        """GET avec cache TTL"""
        cache_key = f"{self.base_url}{endpoint}"
        
        if cache_key in self._cache:
            data, timestamp = self._cache[cache_key]
            if time.time() - timestamp < ttl:
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