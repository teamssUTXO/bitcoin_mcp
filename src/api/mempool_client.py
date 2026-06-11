import logging
from src.api.client import APIClient
from src.config import Config
from returns.result import Result
from src.errors import Error

logger = logging.getLogger(__name__)

class MempoolClient(APIClient):
    def __init__(self):
        super().__init__(Config.MEMPOOL_API_URL)


    # === BITCOIN BLOCKS INFORMATIONS ===

    async def get_block_tip_height(self) -> Result[str, Error]:
        """
        Returns the height of the last block mined on the Bitcoin network
        Docs : https://mempool.space/docs/api/rest#get-block-tip-height
        """
        return await self.get("/blocks/tip/height")

    async def get_block_tip_hash(self) -> Result[str, Error]:
        """
        Returns the hash of the last block mined on the Bitcoin network
        Docs : https://mempool.space/docs/api/rest#get-block-tip-hash
        """
        return await self.get("/blocks/tip/hash")

    async def get_block_height(self, height: int) -> Result[str, Error]:
        """
        Returns the hash of a block whose height is passed as a parameter
        Docs : https://mempool.space/docs/api/rest#get-block-height
        """
        return await self.get(f"/block-height/{height}")

    async def get_blocks_info(self) -> Result[list[dict], Error]:
        """
        Returns information about the last 10 blocks mined on the Bitcoin network
        Docs : https://mempool.space/docs/api/rest#get-blocks
        """
        return await self.get("/v1/blocks")


    # === BITCOIN FEES INFORMATIONS ===

    async def get_recommended_fees(self) -> Result[dict, Error]:
        """
        Returns the recommended transaction fee ratio for a Bitcoin transaction
        Docs : https://mempool.space/docs/api/rest#get-recommended-fees-precise
        """
        return await self.get("/v1/fees/recommended")


    # === BITCOIN ADDRESSES INFORMATIONS ===

    async def get_address_info(self, address: str) -> Result[dict, Error]:
        """
        Returns the information for a Bitcoin address
        Docs : https://mempool.space/docs/api/rest#get-address
        """
        return await self.get(f"/address/{address}")


    # === BITCOIN TRANSACTIONS INFORMATIONS ===

    async def get_tx_info(self, txid: str) -> Result[dict, Error]:
        """
        Returns information about a Bitcoin transaction
        Docs : https://mempool.space/docs/api/rest#get-transaction
        """
        return await self.get(f"/tx/{txid}")


    # === BITCOIN MINING POOLS INFORMATIONS ===

    async def get_mining_pools_rank(self) -> Result[dict, Error]:
        """
        Returns the ranking of the best Bitcoin network mining pools for the last 3 months
        Docs : https://mempool.space/docs/api/rest#get-mining-pools
        """
        return await self.get("/v1/mining/pools/3m")

    async def get_mining_pools_hashrate(self) -> Result[list[dict], Error]:
        """
        Returns the hashrate of the best Bitcoin network mining pools for the last 3 months
        Docs : https://mempool.space/docs/api/rest#get-mining-pool-hashrates
        """
        return await self.get("/v1/mining/hashrate/pools/3m")

    async def get_mining_pool_info_by_slug(self, slug: str) -> Result[dict, Error]:
        """
        Returns information about a mining pool via its slug
        Docs : https://mempool.space/docs/api/rest#get-mining-pool
        """
        return await self.get(f"/v1/mining/pool/{slug}")


    # === BITCOIN NETWORK INFORMATIONS (MEMPOOL) ===

    async def get_mempool_info(self) -> Result[dict, Error]:
        """
        Returns information about the mempool of mempool.space
        Docs : https://mempool.space/docs/api/rest#get-mempool
        """
        return await self.get("/mempool")


# Singleton instance for the client
_mempool_instance = None

def get_mempool_client() -> MempoolClient:
    """Get or create the Mempool API client singleton instance."""
    global _mempool_instance
    if _mempool_instance is None:
        _mempool_instance = MempoolClient()
    return _mempool_instance


async def close_mempool_client() -> None:
    """Close and clear the Mempool API client singleton instance."""
    global _mempool_instance
    if _mempool_instance is not None:
        await _mempool_instance.close()
        _mempool_instance = None
