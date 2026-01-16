from typing import Optional
from src.api.client import APIClient
from src.config import Config

class BlockchainClient(APIClient):
    def __init__(self):
        super().__init__(Config.BLOCKCHAIN_INFO_API_URL)


    # === BITCOIN NETWORK INFORMATIONS ===

    def get_network_hashrate(self) -> Optional[int]:
        """
        Renvoie le hashrate actuel du réseau bitcoin
        Docs : https://blockchain.com/fr/explorer/api/blockchain_api
        """
        result = self.get("/q/hashrate", ttl=30)
        return int(result) if result else None

    def get_network_difficulty(self) -> Optional[float]:
        """
        Renvoie la difficulté actuelle du réseau bitcoin
        Docs : https://blockchain.com/fr/explorer/api/blockchain_api
        """
        result = self.get("/q/getdifficulty", ttl=30)
        return int(result) if result else None

    def get_network_stats(self) -> Optional[dict]:
        """
        Renvoie les stats actuels du réseau bitcoin
        Docs : https://blockchain.com/fr/explorer/api/blockchain_api
        """
        return self.get("/stats?format=json", ttl=30)


    # === BITCOIN TRANSACTIONS INFORMATIONS ===

    def get_nb_tx_day(self) -> Optional[int]:
        """
        Renvoie le nombre de transactions sur 24h
        Docs : https://www.blockchain.com/fr/explorer/api/q
        """
        result = self.get("/q/24hrtransactioncount", ttl=60)
        return int(result) if result else None

    def get_nb_stc_day(self) -> Optional[int]:
        """
        Renvoie le nombre de satoshis envoyés sur 24h
        Docs : https://www.blockchain.com/fr/explorer/api/q
        """
        result = self.get("/q/24hrbtcsent", ttl=60)
        return int(result) if result else None


    # === BITCOIN BLOCKS INFORMATIONS ===

    def get_lastest_block(self) -> Optional[dict]:
        """
        Renvoie les infos du dernier bloc miné
        Docs : https://blockchain.com/fr/explorer/api/blockchain_api
        """
        return self.get("/lastestblock", ttl=60)


    # === BITCOIN ADDRESSES INFORMATIONS ===

    def get_address_info(self, address) -> Optional[dict]:
        """
        Renvoie les infos d'une adresse
        Docs : "https://www.blockchain.com/fr/explorer/api/blockchain_api"
        """
        return self.get(f"/rawaddr/{address}", ttl=60)

