from typing import Optional
from src.api.client import APIClient
from src.config import Config

class MempoolClient(APIClient):
    def __init__(self):
        super().__init__(Config.MEMPOOL_API_URL)


    # === BITCOIN BLOCKS INFORMATIONS ===

    def get_block_tip_height(self) -> Optional[int]:
        """
        Renvoie la hauteur du dernier bloc
        Docs : https://mempool.space/docs/api/rest#get-block-tip-height
        """
        result = self.get("/blocks/tip/height")
        return str(result) if result else None

    def get_block_tip_hash(self) -> Optional[int]:
        """
        Renvoie le hash du dernier bloc
        Docs : https://mempool.space/docs/api/rest#get-block-tip-hash
        """
        result = self.get("/blocks/tip/hash",)
        return str(result) if result else None

    def get_block_height(self, height: int) -> Optional[str]:
        """
        Renvoie le hash d'un bloc dont la hauteur est passé en paramètre
        Docs : https://mempool.space/docs/api/rest#get-block-height
        """
        return str(self.get(f"/block-height/{height}"))

    def get_blocks_info(self) -> Optional[list[dict]]:
        """
        Renvoie des infos sur les 10 derniers blocs
        Docs : https://mempool.space/docs/api/rest#get-blocks
        """
        return self.get("/v1/blocks")


    # === BITCOIN FEES INFORMATIONS ===

    def get_recommended_fees(self) -> Optional[dict]:
        """
        Renvoie le ratio de frais de transactions recommandés
        Docs : https://mempool.space/docs/api/rest#get-recommended-fees-precise
        """
        return self.get("/v1/fees/recommended")


    # === BITCOIN ADDRESSES INFORMATIONS ===

    def get_address_info(self, address: str) -> Optional[dict]:
        """
        Renvoie les infos d'une adresse bitcoin
        Docs : https://mempool.space/docs/api/rest#get-address
        """
        return self.get(f"/address/{address}")


    # === BITCOIN TRANSACTIONS INFORMATIONS ===

    def get_tx_info(self, txid: str) -> Optional[dict]:
        """
        Renvoie des infos sur une transaction
        Docs : https://mempool.space/docs/api/rest#get-transaction
        """
        return self.get(f"/tx/{txid}")


    # === BITCOIN MINING POOLS INFORMATIONS ===

    def get_mining_pools_rank(self) -> Optional[dict]:
        """
        Renvoie le classement des meilleures mining pools depuis 3 mois
        Docs : https://mempool.space/docs/api/rest#get-mining-pools
        """
        return self.get("/v1/mining/pools/3m")

    def get_mining_pools_hashrate(self) -> Optional[list]:
        """
        Renvoie le hashrate des meilleures mining pools depuis 3 mois
        Docs : https://mempool.space/docs/api/rest#get-mining-pool-hashrates
        """
        return self.get("/v1/mining/hashrate/pools/3m")

    def get_mining_pool_info_by_slug(self, slug: str) -> Optional[dict]:
        """
        Renvoie les infos d'un mining pool (via slug)
        Docs : https://mempool.space/docs/api/rest#get-mining-pool
        """
        return self.get(f"/v1/mining/pool/{slug}")


    # === BITCOIN NETWORK INFORMATIONS (MEMPOOL) ===

    def get_mempool_info(self) -> Optional[dict]:
        """
        Renvoie des infos sur la mempool de mempool.space
        Docs : https://mempool.space/docs/api/rest#get-mempool
        """
        return self.get("/mempool")


# Singleton instance for the client
_mempool_instance = None


def get_mempool_client() -> MempoolClient:
    """Get or create the Elfa API client singleton instance."""
    global _mempool_instance
    if _mempool_instance is None:
        _mempool_instance = MempoolClient()
    return _mempool_instance