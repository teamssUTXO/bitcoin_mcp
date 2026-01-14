from typing import Optional
from src.api.client import APIClient
from src.config import Config

class BlockchainClient(APIClient):
    def __init__(self):
        super().__init__(Config.BLOCKCHAIN_INFO_API_URL)
    
    """
    Renvoie le hashrate actuel du réseau bitcoin
    Docs : https://blockchain.com/fr/explorer/api/blockchain_api
    """
    def get_network_hashrate(self) -> Optional[int]:
        result = self.get("/q/hashrate", ttl=30)
        return int(result) if result else None


    """
    Renvoie la difficulté actuelle du réseau bitcoin
    Docs : https://blockchain.com/fr/explorer/api/blockchain_api
    """
    def get_network_difficulty(self) -> Optional[float]:
        result = self.get("/q/getdifficulty", ttl=30)
        return int(result) if result else None


    """
    Renvoie le nombre de transactions sur 24h
    Docs : https://www.blockchain.com/fr/explorer/api/q
    """
    def get_nb_tx_day(self) -> Optional[int]:
        result = self.get("/q/24hrtransactioncount", ttl=60)
        return int(result) if result else None


    """
    Renvoie le nombre de satoshis envoyés sur 24h
    Docs : https://www.blockchain.com/fr/explorer/api/q
    """
    def get_nb_stc_day(self) -> Optional[int]:
        result = self.get("/q/24hrbtcsent", ttl=60)
        return int(result) if result else None


    """
    Renvoie les stats actuels du réseau bitcoin
    Docs : https://blockchain.com/fr/explorer/api/blockchain_api
    """
    def get_network_stats(self) -> Optional[dict]:
        return self.get("/stats?format=json", ttl=30)


    """
    Renvoie les infos du dernier bloc actuel
    Docs : https://blockchain.com/fr/explorer/api/blockchain_api
    """
    def get_lastest_block(self) -> Optional[dict]:
        return self.get("/lastestblock", ttl=60)


    """
    Renvoie les infos d'une adresse
    Docs : "https://www.blockchain.com/fr/explorer/api/blockchain_api"
    """
    def get_address_info(self, address) -> Optional[dict]:
        return self.get(f"/rawaddr/{address}", ttl=60)

