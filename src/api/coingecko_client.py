from typing import Optional
from client import APIClient
from ..config import Config

class CoinGeckoClient(APIClient):
    def __init__(self):
        super().__init__(Config.COINGECKO_API_URL)
    
    """"Renvoie des données globales sur le marché des cryptomonnaies"""
    def get_global_market_data(self) -> Optional[dict]:
        return self.get("/global", ttl=30)
    
    """"Renvoie le prix du bitcoin en USD"""
    def get_btc_price_usd(self) -> Optional[dict]:
        return self.get("/simple/price?ids=bitcoin&vs_currencies=usd", ttl=30)
    
    """"Renvoie le prix, le market cap, le volume, la variation sur 24h, l'ATH/ATL, le rang du marché, la supply (circulating, total, max), la fully diluted valuation, la last updated et des informations générales (nom, symbol, image)"""
    def get_market_data(self) -> Optional[dict]:
        return self.get("/coins/bitcoin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false", ttl=45)
    