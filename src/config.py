import os
from dataclasses import dataclass

@dataclass
class Config:
    # API URLs
    MEMPOOL_API_URL: str = "https://mempool.space/api"
    COINGECKO_API_URL: str = "https://api.coingecko.com/api/v3"
    BLOCKCHAIN_INFO_API_URL: str = "https://blockchain.info"
    HIRO_API_URL: str = "https://api.hiro.so"
    ALTERNATIVE_API_URL: str = "https://api.alternative.me"

    SATOSHI: int = 100_000_000

    # Timeouts in seconds
    API_TIMEOUT: int = 5
    CACHE_TTL_TIME: int = 30

    # # Features
    # ENABLE_CACHE: bool = True
    # ENABLE_RETRY: bool = True
    # MAX_RETRIES: int = 3

config = Config()