import os
from dataclasses import dataclass

@dataclass
class Config:
    # API URLs
    MEMPOOL_API_URL: str = "https://mempool.space/api"
    COINGECKO_API_URL: str = "https://api.coingecko.com/api/v3"
    BLOCKCHAIN_INFO_API_URL: str = "https://blockchain.info"
    HIRO_API_URL: str = "https://api.hiro.so/ordinals/v1"
    ALTERNATIVE_API_URL: str = "https://api.alternative.me/"
    
    # # Timeouts in seconds
    # API_TIMEOUT: int = 5
    # CACHE_TTL_SHORT: int = 30
    # CACHE_TTL_MEDIUM: int = 60
    # CACHE_TTL_LONG: int = 300
    
    # # Features
    # ENABLE_CACHE: bool = True
    # ENABLE_RETRY: bool = True
    # MAX_RETRIES: int = 3

config = Config()