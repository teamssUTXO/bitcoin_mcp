import logging
from src.api.client import APIClient
from src.config import Config
from returns.result import Result
from src.errors import Error

logger = logging.getLogger(__name__)

class AlternativeClient(APIClient):
    def __init__(self):
        super().__init__(Config.ALTERNATIVE_API_URL)


    # === BITCOIN NETWORK INFORMATIONS ===

    async def get_global_cryptomarket_infos(self) -> Result[dict, Error]:
        """
        Unused

        Returns information on the cryptocurrency market
        Docs : https://alternative.me/crypto/api/
        """
        return await self.get("/v2/global")

    async def get_fear_greed_index(self) -> Result[dict, Error]:
        """
        Returns the 'Fear & Greed' index on the crypto market over 7 days
        Docs : https://alternative.me/crypto/fear-and-greed-index/#api
        """
        return await self.get("/fng/?limit=7")


# Singleton instance for the client
_alternative_instance = None

def get_alternative_client() -> AlternativeClient:
    """Get or create the Alternative API client singleton instance."""
    global _alternative_instance
    if _alternative_instance is None:
        _alternative_instance = AlternativeClient()
    return _alternative_instance


async def close_alternative_client() -> None:
    """Close and clear the Alternative API client singleton instance."""
    global _alternative_instance
    if _alternative_instance is not None:
        await _alternative_instance.close()
        _alternative_instance = None
