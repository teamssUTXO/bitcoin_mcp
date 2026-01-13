from typing import Optional
from .client import APIClient
from ..config import Config

class HiroClient(APIClient):
    def __init__(self):
        super().__init__(Config.HIRO_API_URL)
    
    """Renvoie les ordinals d'une adresse bitcoin"""
    def get_address_ordinals_inscription(self, address) -> Optional[dict]:
        return self.get(f"/inscriptions?address={address}&limit=5", ttl=30)
        
    """Renvoie le solde bitcoin d'une adresse"""
    def get_address_balance(self, address) -> Optional[dict]:
        return self.get(f"/account/{address}/balances", ttl=30)