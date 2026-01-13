from typing import Optional
from .client import APIClient
from ..config import Config

class BlockchainClient(APIClient):
    def __init__(self):
        super().__init__(Config.BLOCKCHAIN_INFO_API_URL)
    
    """Renvoie le hashrate actuel du réseau bitcoin"""
    def get_network_hashrate(self) -> Optional[dict]:
        return self.get("/q/hashrate", ttl=30)
    
    """Renvoie la difficulté actuelle du réseau bitcoin"""
    def get_network_difficulty(self) -> Optional[dict]:
        return self.get("/q/getdifficulty", ttl=30)
    
    """Renvoie les stats actuels du réseau bitcoin"""
    def get_network_stats(self) -> Optional[dict]:
        return self.get("/stats?format=json", ttl=30)
    
    """Renvoie les infos d'une adresse bitcoin"""
    def get_address_info(self, address: str) -> Optional[dict]:
        return self.get(f"/address/{address}", ttl=60)