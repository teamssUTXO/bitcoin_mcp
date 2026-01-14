from typing import Optional
from src.api.client import APIClient
from src.config import Config

class MempoolClient(APIClient):
    def __init__(self):
        super().__init__(Config.MEMPOOL_API_URL)
    
    """
    Renvoie la hauteur du dernier bloc
    Docs : https://mempool.space/docs/api/rest#get-block-tip-height
    """
    def get_block_tip_height(self) -> Optional[int]:
        result = self.get("/blocks/tip/height", ttl=10)
        return int(result) if result else None


    """
    Renvoie le hash du dernier bloc
    Docs : https://mempool.space/docs/api/rest#get-block-tip-hash
    """
    def get_block_tip_hash(self) -> Optional[int]:
        result = self.get("/blocks/tip/hash", ttl=10)
        return int(result) if result else None


    """
    Renvoie le hash d'un bloc dont la hauteur est passé en paramètre
    Docs : https://mempool.space/docs/api/rest#get-block-height
    """
    def get_block_height(self, height) -> Optional[int]:
        result = self.get(f"/block-height/{height}", ttl=10)
        return int(result) if result else None


    """
    Renvoie le ratio de frais de transactions recommandés
    Docs : https://mempool.space/docs/api/rest#get-recommended-fees-precise
    """
    def get_recommended_fees(self) -> Optional[dict]:
        return self.get("/v1/fees/recommended/precise", ttl=30)


    """
    Renvoie des infos sur la mempool
    Docs : https://mempool.space/docs/api/rest#get-mempool
    """
    def get_mempool_info(self) -> Optional[dict]:
        return self.get("/mempool", ttl=30)


    """
    Renvoie les infos d'une adresse bitcoin
    Docs : https://mempool.space/docs/api/rest#get-address
    """
    def get_address_info(self, address: str) -> Optional[dict]:
        return self.get(f"/address/{address}", ttl=60)


    """
    Renvoie des infos sur une transaction
    Docs : https://mempool.space/docs/api/rest#get-transaction
    """
    def get_tx_info(self, txid: str) -> Optional[dict]:
        return self.get(f"/tx/{txid}", ttl=30)


    """
    Renvoie des infos sur les 10 derniers blocs
    Docs : https://mempool.space/docs/api/rest#get-blocks
    """
    def get_block_info(self) -> Optional[dict]:
        return self.get("/v1/blocks", ttl=30)

    """
    Renvoie le classement des meilleures mempools depuis 3 mois
    Docs : https://mempool.space/docs/api/rest#get-mining-pools
    """
    def get_mempools_rank(self) -> Optional[dict]:
        return self.get("/v1/mining/pools/3m", ttl=30)

    """
    Renvoie le hashrate des meilleures mempools depuis 3 mois
    Docs : https://mempool.space/docs/api/rest#get-mining-pools-hashrates
    """
    def get_hashrate_mempools(self) -> Optional[dict]:
        return self.get("/v1/mining/hashrate/pools/3m", ttl=30)