from typing import Optional
from src.api.client import APIClient
from src.config import Config

class HiroClient(APIClient):
    def __init__(self):
        super().__init__(Config.HIRO_API_URL)
    
    """
    Renvoie les ordinals d'une adresse bitcoin
    Docs : https://docs.hiro.so/en/apis/ordinals-api/reference/inscriptions/get-inscriptions
    """
    def get_address_ordinals_inscription(self, address) -> Optional[dict]:
        return self.get(f"/inscriptions?address={address}&limit=5", ttl=30)
        
    """
    Renvoie le solde bitcoin d'une adresse
    Docs : https://docs.hiro.so/en/apis/stacks-blockchain-api/reference/accounts/balances
    """
    def get_address_balance(self, address) -> Optional[dict]:
        return self.get(f"/account/{address}/balances", ttl=30)