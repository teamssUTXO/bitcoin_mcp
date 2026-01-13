from typing import Optional
from client import APIClient
from ..config import Config

class MempoolClient(APIClient):
    def __init__(self):
        super().__init__(Config.MEMPOOL_API_URL)
    
    """Hauteur du bloc actuel"""
    def get_block_tip_height(self) -> Optional[int]:
        result = self.get("/blocks/tip/height", ttl=10)
        return int(result) if result else None
    
    """Hauteur du dernier bloc"""
    def get_block_height(self) -> Optional[int]:
        result = self.get("/block-height")
        return int(result) if result else None
    
    """Renvoie le ratio de frais de transactions recommandés"""
    def get_recommended_fees(self) -> Optional[dict]:
        return self.get("/v1/fees/recommended", ttl=30)
    
    """Renvoie des infos sur la mempool"""
    def get_mempool_info(self) -> Optional[dict]:
        return self.get("/mempool", ttl=30)
    
    """Renvoie les infos d'une adresse bitcoin"""
    def get_address_info(self, address: str) -> Optional[dict]:
        return self.get(f"/address/{address}", ttl=60)
    
    """Renvoie des infos sur le block miné par la mempool (backlog)"""
    def get_mempool_block_info(self) -> Optional[dict]:
        return self.get("/mempool/blocks", ttl=30)
    
    """Renvoie des infos sur une transaction"""
    def get_tx_info(self, txid: str) -> Optional[dict]:
        return self.get(f"/tx/{txid}", ttl=30)
    
    """Renvoie des infos sur le bloc actuel"""
    def get_block_info(self) -> Optional[dict]:
        return self.get("/v1/blocks", ttl=30)