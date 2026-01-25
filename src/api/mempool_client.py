import logging
from typing import Optional
from src.api.client import APIClient
from src.config import Config

logger = logging.getLogger(__name__)

class MempoolClient(APIClient):
    def __init__(self):
        super().__init__(Config.MEMPOOL_API_URL)


    # === BITCOIN BLOCKS INFORMATIONS ===

    def get_block_tip_height(self) -> Optional[int]:
        """
        Returns the height of the last block mined on the Bitcoin network
        Docs : https://mempool.space/docs/api/rest#get-block-tip-height
        """
        try:
            result = self.get("/blocks/tip/height")
            return str(result) if result else None
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None

    def get_block_tip_hash(self) -> Optional[int]:
        """
        Returns the hash of the last block mined on the Bitcon network
        Docs : https://mempool.space/docs/api/rest#get-block-tip-hash
        """
        try:
            result = self.get("/blocks/tip/hash",)
            return str(result) if result else None
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None

    def get_block_height(self, height: int) -> Optional[str]:
        """
        Returns the hash of a block whose height is passed as a parameter
        Docs : https://mempool.space/docs/api/rest#get-block-height
        """
        try:
            return str(self.get(f"/block-height/{height}"))
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None

    def get_blocks_info(self) -> Optional[list[dict]]:
        """
        Returns information about the last 10 blocks mined on the Bitcoin network
        Docs : https://mempool.space/docs/api/rest#get-blocks
        """
        try:
            return self.get("/v1/blocks")
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None


    # === BITCOIN FEES INFORMATIONS ===

    def get_recommended_fees(self) -> Optional[dict]:
        """
        Returns the recommended transaction fee ratio for a Bitcoin transaction
        Docs : https://mempool.space/docs/api/rest#get-recommended-fees-precise
        """
        try:
            return self.get("/v1/fees/recommended")
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None


    # === BITCOIN ADDRESSES INFORMATIONS ===

    def get_address_info(self, address: str) -> Optional[dict]:
        """
        Returns the information for a Bitcoin address
        Docs : https://mempool.space/docs/api/rest#get-address
        """
        try:
            return self.get(f"/address/{address}")
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None


    # === BITCOIN TRANSACTIONS INFORMATIONS ===

    def get_tx_info(self, txid: str) -> Optional[dict]:
        """
        Returns information about a Bitcoin transaction
        Docs : https://mempool.space/docs/api/rest#get-transaction
        """
        try:
            return self.get(f"/tx/{txid}")
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None


    # === BITCOIN MINING POOLS INFORMATIONS ===

    def get_mining_pools_rank(self) -> Optional[dict]:
        """
        Returns the ranking of the best Bitcoin network mining pools for the last 3 months
        Docs : https://mempool.space/docs/api/rest#get-mining-pools
        """
        try:
            return self.get("/v1/mining/pools/3m")
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None

    def get_mining_pools_hashrate(self) -> Optional[list]:
        """
        Renvoie le hashrate des meilleures mining pools du réseau bitcoin depuis 3 mois
        Docs : https://mempool.space/docs/api/rest#get-mining-pool-hashrates
        """
        try:
            return self.get("/v1/mining/hashrate/pools/3m")
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None

    def get_mining_pool_info_by_slug(self, slug: str) -> Optional[dict]:
        """
        Returns information about a mining pool via its slug
        Docs : https://mempool.space/docs/api/rest#get-mining-pool
        """
        try:
            return self.get(f"/v1/mining/pool/{slug}")
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None


    # === BITCOIN NETWORK INFORMATIONS (MEMPOOL) ===

    def get_mempool_info(self) -> Optional[dict]:
        """
        Returns information about the mempool of mempool.space
        Docs : https://mempool.space/docs/api/rest#get-mempool
        """
        try:
            return self.get("/mempool")
        except Exception as e:
            logger.error(f"Failed to fetch data from Mempool.space : {e}")
            return None


# Singleton instance for the client
_mempool_instance = None

def get_mempool_client() -> MempoolClient:
    """Get or create the Elfa API client singleton instance."""
    global _mempool_instance
    if _mempool_instance is None:
        _mempool_instance = MempoolClient()
    return _mempool_instance