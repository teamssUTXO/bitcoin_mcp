import logging
from typing import Optional
from src.api.client import APIClient
from src.config import Config

logger = logging.getLogger(__name__)

class AlternativeClient(APIClient):
    def __init__(self):
        super().__init__(Config.ALTERNATIVE_API_URL)


    # === BITCOIN NETWORK INFORMATIONS ===

    def get_global_cryptomarket_infos(self) -> Optional[dict]:
        """
        Unused

        Returns information on the cryptocurrency market
        Docs : https://alternative.me/crypto/api/
        """
        try:
            return self.get("/v2/global")
        except Exception as e:
            logger.error(f"Failed to fetch data from Alternative : {e}")
            return None

    def get_fear_greed_index(self) -> Optional[dict]:
        """
        Returns the 'Fear & Greed' index on the crypto market over 7 days
        Docs : https://alternative.me/crypto/fear-and-greed-index/#api
        """
        try:
            return self.get("/fng/?limit=7")
        except Exception as e:
            logger.error(f"Failed to fetch data from Alternative : {e}")
            return None


# Singleton instance for the client
_alternative_instance = None

def get_alternative_client() -> AlternativeClient:
    """Get or create the Alternative API client singleton instance."""
    global _alternative_instance
    if _alternative_instance is None:
        _alternative_instance = AlternativeClient()
    return _alternative_instance