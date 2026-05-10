import logging
from src.api.client import APIClient
from src.config import Config
from returns.result import Result
from src.errors import Error

logger = logging.getLogger(__name__)

class BlockchainClient(APIClient):
    def __init__(self):
        super().__init__(Config.BLOCKCHAIN_INFO_API_URL)


    async def get_network_stats(self) -> Result[dict, Error]:
        """
        Returns current Bitcoin network stats
        Docs : https://blockchain.com/fr/explorer/api/blockchain_api
        """
        return await self.get("/stats?format=json")


    # === BITCOIN NETWORK INFORMATIONS ===

    async def get_network_hashrate(self) -> Result[int, Error]:
        """
        Unused

        Returns the current hashrate of the Bitcoin network miners
        Docs : https://www.blockchain.com/fr/explorer/api/q
        """
        return await self.get("/q/hashrate")

    async def get_network_difficulty(self) -> Result[float, Error]:
        """
        Unused

        Returns the current difficulty of the bitcoin network
        Docs : https://www.blockchain.com/fr/explorer/api/q
        """
        return await self.get("/q/getdifficulty")


    # === BITCOIN TRANSACTIONS INFORMATIONS ===

    async def get_nb_tx_day(self) -> Result[int, Error]:
        """
        Unused

        Returns the number of transactions in the Bitcoin network over 24 hours
        Docs : https://www.blockchain.com/fr/explorer/api/q
        """
        return await self.get("/q/24hrtransactioncount")

    async def get_nb_stc_day(self) -> Result[int, Error]:
        """
        Unused

        Returns the number of satoshis sent on the Bitcoin network in 24 hours
        Docs : https://www.blockchain.com/fr/explorer/api/q
        """
        return await self.get("/q/24hrbtcsent")

    async def get_unconfirmed_tx(self) -> Result[int, Error]:
        """
        Unused

        Returns the number of unconfirmed transactions on the Bitcoin network
        Docs : https://www.blockchain.com/fr/explorer/api/q
        """
        return await self.get("/q/unconfirmedcount")


    # === BITCOIN BLOCKS INFORMATIONS ===

    async def get_latest_block(self) -> Result[dict, Error]:
        """
        Returns information about the last mined block on the Bitcoin network
        Docs : "https://www.blockchain.com/fr/explorer/api/blockchain_api"
        """
        return await self.get("/latestblock")


    # === BITCOIN ADDRESSES INFORMATIONS ===

    async def get_address_info(self, address: str) -> Result[dict, Error]:
        """
        Returns the information for a Bitcoin address (param address in base58 or hash160)
        Docs : "https://www.blockchain.com/fr/explorer/api/blockchain_api"
        """
        return await self.get(f"/rawaddr/{address}")


# Singleton instance for the client
_blockchain_instance = None

def get_blockchain_client() -> BlockchainClient:
    """Get or create the Blockchain.com API client singleton instance."""
    global _blockchain_instance
    if _blockchain_instance is None:
        _blockchain_instance = BlockchainClient()
    return _blockchain_instance


async def close_blockchain_client() -> None:
    """Close and clear the Blockchain.com API client singleton instance."""
    global _blockchain_instance
    if _blockchain_instance is not None:
        await _blockchain_instance.close()
        _blockchain_instance = None
