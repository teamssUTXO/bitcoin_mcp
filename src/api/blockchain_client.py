from typing import Optional
from src.api.client import APIClient
from src.config import Config

class BlockchainClient(APIClient):
    def __init__(self):
        super().__init__(Config.BLOCKCHAIN_INFO_API_URL)
    
    """
    Renvoie le hashrate actuel du réseau bitcoin
    Docs : https://blockchain.com/fr/explorer/api/blockchain_api
    """
    def get_network_hashrate(self) -> Optional[int]:
        result = self.get("/q/hashrate", ttl=30)
        return int(result) if result else None


    """
    Renvoie la difficulté actuelle du réseau bitcoin
    Docs : https://blockchain.com/fr/explorer/api/blockchain_api
    """
    def get_network_difficulty(self) -> Optional[float]:
        result = self.get("/q/getdifficulty", ttl=30)
        return int(result) if result else None


    """
    Renvoie les stats actuels du réseau bitcoin
    Docs : https://blockchain.com/fr/explorer/api/blockchain_api
    """
    def get_network_stats(self) -> Optional[dict]:
        return self.get("/stats?format=json", ttl=30)


    """
    Renvoie les infos d'une adresse bitcoin
    Docs : https://blockchain.com/fr/explorer/api/blockchain_api
    """
    def get_address_info(self, address: str) -> Optional[dict]:
        return self.get(f"/address/{address}", ttl=60)