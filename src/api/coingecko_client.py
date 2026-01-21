from typing import Optional
from src.api.client import APIClient
from src.config import Config


class CoinGeckoClient(APIClient):
    def __init__(self):
        super().__init__(Config.COINGECKO_API_URL)


    # === GLOBAL MARKET INFORMATIONS ===

    def get_global_market_data(self) -> Optional[dict]:
        """
        Renvoie des données globales sur le marché des cryptomonnaies
        Docs : https://docs.coingecko.com/reference/crypto-global
        """
        return self.get("/global")

    def get_market_trend(self) -> Optional[dict]:
        """
        Renvoie les tendances du marché des cryptomonnaies
        Top 15 trending coins
        Top 7 trending NFTs
        Top 6 trending categories
        sorted by the most popular user searches
        Docs : https://docs.coingecko.com/reference/coins-id
        """
        return self.get("/search/trending")


    # === GLOBAL INFORMATIONS ABOUT BITCOIN ===

    def get_btc_market_data(self) -> Optional[dict]:
        """
        Renvoie des informations générales sur le bitcoin
        Docs : https://docs.coingecko.com/reference/coins-id
        """
        return self.get("/coins/bitcoin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false")

    def get_btc_price_usd(self) -> Optional[dict]:
        """
        Renvoie le prix du bitcoin en USD
        Docs : https://docs.coingecko.com/reference/simple-price
        """
        return self.get("/simple/price?ids=bitcoin&vs_currencies=usd")


# Singleton instance for the client
_coingecko_instance = None


def get_coingecko_client() -> CoinGeckoClient:
    """Get or create the Elfa API client singleton instance."""
    global _coingecko_instance
    if _coingecko_instance is None:
        _coingecko_instance = CoinGeckoClient()
    return _coingecko_instance