import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    # API URLs
    MEMPOOL_API_URL: str = "https://mempool.space/api"
    COINGECKO_API_URL: str = "https://api.coingecko.com/api/v3"
    BLOCKCHAIN_INFO_API_URL: str = "https://blockchain.info"
    HIRO_API_URL: str = "https://api.hiro.so"
    ALTERNATIVE_API_URL: str = "https://api.alternative.me"

    SATOSHI: int = 100_000_000

    # Retry & Cache
    ENABLE_CACHE: bool = True
    ENABLE_RETRY: bool = True

    # APIs Management

    CACHE_TTL_TIME: int = 60
    MAX_RETRIES: int = 3

    # Timeout
    API_CONNECT_TIMEOUT: int = 5.0
    API_READ_TIMEOUT: int = 30.0
    API_WRITE_TIMEOUT: int = 10.0
    API_POOL_TIMEOUT: int = 5.0

    # Logging
    LOGGER_NAME: str = "bitcoin_mcp_server"
    LOG_DIR: str = "../logs"
    LOG_LEVEL: str = "INFO"
    LOGGER_BACKUP_COUNT: int = 30
    LOGGER_CONSOLE_OUTPUT: bool = True


config = Config()