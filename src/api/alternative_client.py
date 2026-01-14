from typing import Optional
from src.api.client import APIClient
from src.config import Config

class AlternativeClient(APIClient):
    def __init__(self):
        super().__init__(Config.ALTERNATIVE_API_URL)
    
    """
    Renvoie des infos sur le marché des crytomonnaies
    Docs : https://alternative.me/crypto/api/
    """
    def get_global_cryptomarket_infos(self) -> Optional[dict]:
        return self.get("/v2/global", ttl=30)


    """
    Renvoie l'indice 'Fear & Greed' sur le marché crypto sur 7 jours
    Docs : https://alternative.me/crypto/fear-and-greed-index/#api
    """
    def get_fear_greed_index(self) -> Optional[dict]:
        return self.get("/fng/?limit=7", ttl=30)

