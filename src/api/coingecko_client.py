import logging
from typing import Optional
from src.api.client import APIClient
from src.config import Config

logger = logging.getLogger(__name__)

class CoinGeckoClient(APIClient):
    def __init__(self):
        super().__init__(Config.COINGECKO_API_URL)


    # === GLOBAL MARKET INFORMATIONS ===

    async def get_global_market_data(self) -> Optional[dict]:
        """
        Returns global data on the cryptocurrency market
        Docs : https://docs.coingecko.com/reference/crypto-global
        """
        try:
            return await self.get("/global")
        except Exception as e:
            logger.error(f"Failed to fetch data from CoinGecko : {e}")
            return None

    async def get_market_trend(self) -> Optional[dict]:
        """
        Returns cryptocurrency market trends sorted by the most popular user searches :
        - Top 15 trending coins
        - Top 7 trending NFTs
        - Top 6 trending categories
        Docs : https://docs.coingecko.com/reference/trending-search
        """
        try:
            return await self.get("/search/trending")
        except Exception as e:
            logger.error(f"Failed to fetch data from CoinGecko : {e}")
            return None


    # === GLOBAL INFORMATIONS ABOUT BITCOIN ===

    async def get_btc_market_data(self) -> Optional[dict]:
        """
        Returns general information about Bitcoin
        Docs : https://docs.coingecko.com/reference/coins-id
        """
        try:
            return await self.get("/coins/bitcoin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false")
        except Exception as e:
            logger.error(f"Failed to fetch data from CoinGecko : {e}")
            return None

    async def get_btc_price_usd(self) -> Optional[dict]:
        """
        Returns the price of Bitcoin in USD
        Docs : https://docs.coingecko.com/reference/simple-price
        """
        try:
            return await self.get("/simple/price?ids=bitcoin&vs_currencies=usd")
        except Exception as e:
            logger.error(f"Failed to fetch data from CoinGecko : {e}")
            return None


# Singleton instance for the client
_coingecko_instance = None

def get_coingecko_client() -> CoinGeckoClient:
    """Get or create the CoinGecko API client singleton instance."""
    global _coingecko_instance
    if _coingecko_instance is None:
        _coingecko_instance = CoinGeckoClient()
    return _coingecko_instance


async def close_coingecko_client() -> None:
    """Close and clear the CoinGecko API client singleton instance."""
    global _coingecko_instance
    if _coingecko_instance is not None:
        await _coingecko_instance.close()
        _coingecko_instance = None
