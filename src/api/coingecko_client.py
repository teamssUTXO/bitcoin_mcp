from typing import Optional
from src.api.client import APIClient
from src.config import Config

# TODO : implementer l'endpoint des trendings coins
class CoinGeckoClient(APIClient):
    def __init__(self):
        super().__init__(Config.COINGECKO_API_URL)


    # === GLOBAL MARKET INFORMATIONS ===
    
    """"
    Renvoie des données globales sur le marché des cryptomonnaies
    Docs : https://docs.coingecko.com/reference/crypto-global
    """
    def get_global_market_data(self) -> Optional[dict]:
        return self.get("/global", ttl=30)

    """"
    Renvoie des trending coins
    Docs : https://docs.coingecko.com/reference/coins-id
    """
    def get_trending_coins(self) -> Optional[dict]:
        return self.get("/search/trending",ttl=45)


    # === GLOBAL INFORMATIONS ABOUT BITCOIN ===

    """"
    Renvoie des informations générales sur le bitcoin
    Docs : https://docs.coingecko.com/reference/coins-id
    """
    def get_btc_market_data(self) -> Optional[dict]:
        return self.get("/coins/bitcoin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false", ttl=45)

    """"
    Renvoie le prix du bitcoin en USD
    Docs : https://docs.coingecko.com/reference/simple-price
    """
    def get_btc_price_usd(self) -> Optional[dict]:
        return self.get("/simple/price?ids=bitcoin&vs_currencies=usd", ttl=30)

