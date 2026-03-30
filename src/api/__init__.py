import asyncio

from src.api.alternative_client import close_alternative_client
from src.api.blockchain_client import close_blockchain_client
from src.api.coingecko_client import close_coingecko_client
from src.api.mempool_client import close_mempool_client


async def close_all_api_clients() -> None:
    """Close all API client singletons concurrently."""
    await asyncio.gather(
        close_mempool_client(),
        close_coingecko_client(),
        close_blockchain_client(),
        close_alternative_client(),
    )
