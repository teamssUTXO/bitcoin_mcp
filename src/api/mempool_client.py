from typing import Optional
from src.api.client import APIClient
from src.config import Config

class MempoolClient(APIClient):
    def __init__(self):
        super().__init__(Config.MEMPOOL_API_URL)


    # === BITCOIN BLOCKS INFORMATIONS ===

    def get_block_tip_height(self) -> Optional[int]:
        """
        Returns the height of the last block mined on the Bitcoin network
        Docs : https://mempool.space/docs/api/rest#get-block-tip-height
        """
        result = self.get("/blocks/tip/height")
        return str(result) if result else None

    def get_block_tip_hash(self) -> Optional[int]:
        """
        Returns the hash of the last block mined on the Bitcon network
        Docs : https://mempool.space/docs/api/rest#get-block-tip-hash
        """
        result = self.get("/blocks/tip/hash",)
        return str(result) if result else None

    def get_block_height(self, height: int) -> Optional[str]:
        """
        Returns the hash of a block whose height is passed as a parameter
        Docs : https://mempool.space/docs/api/rest#get-block-height
        """
        return str(self.get(f"/block-height/{height}"))

    def get_blocks_info(self) -> Optional[list[dict]]:
        """
        Returns information about the last 10 blocks mined on the Bitcoin network
        Docs : https://mempool.space/docs/api/rest#get-blocks
        """
        return self.get("/v1/blocks")


    # === BITCOIN FEES INFORMATIONS ===

    def get_recommended_fees(self) -> Optional[dict]:
        """
        Returns the recommended transaction fee ratio for a Bitcoin transaction
        Docs : https://mempool.space/docs/api/rest#get-recommended-fees-precise
        """
        return self.get("/v1/fees/recommended")


    # === BITCOIN ADDRESSES INFORMATIONS ===

    def get_address_info(self, address: str) -> Optional[dict]:
        """
        Returns the information for a Bitcoin address
        Docs : https://mempool.space/docs/api/rest#get-address
        """
        return self.get(f"/address/{address}")


    # === BITCOIN TRANSACTIONS INFORMATIONS ===

    def get_tx_info(self, txid: str) -> Optional[dict]:
        """
        Returns information about a Bitcoin transaction
        Docs : https://mempool.space/docs/api/rest#get-transaction
        """
        return self.get(f"/tx/{txid}")


    # === BITCOIN MINING POOLS INFORMATIONS ===

    def get_mining_pools_rank(self) -> Optional[dict]:
        """
        Returns the ranking of the best Bitcoin network mining pools for the last 3 months
        Docs : https://mempool.space/docs/api/rest#get-mining-pools
        """
        return self.get("/v1/mining/pools/3m")

    def get_mining_pools_hashrate(self) -> Optional[list]:
        """
        Renvoie le hashrate des meilleures mining pools du réseau bitcoin depuis 3 mois
        Docs : https://mempool.space/docs/api/rest#get-mining-pool-hashrates
        """
        return self.get("/v1/mining/hashrate/pools/3m")

    def get_mining_pool_info_by_slug(self, slug: str) -> Optional[dict]:
        """
        Returns information about a mining pool via its slug
        Docs : https://mempool.space/docs/api/rest#get-mining-pool
        """
        return self.get(f"/v1/mining/pool/{slug}")


    # === BITCOIN NETWORK INFORMATIONS (MEMPOOL) ===

    def get_mempool_info(self) -> Optional[dict]:
        """
        Returns information about the mempool of mempool.space
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