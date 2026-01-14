from typing import Dict, Optional
from src.api.mempool_client import MempoolClient
from src.api.blockchain_client import BlockchainClient


class NetworkAnalyzer:
    def __init__(self):
        self.mempool = MempoolClient()
        self.blockchain = BlockchainClient()
    
    def get_network_overview(self) -> Dict:
        """Agrège les données réseau depuis plusieurs sources"""
        block_height = self.mempool.get_block_tip_height()
        hashrate = self.blockchain.get_network_hashrate()
        difficulty = self.blockchain.get_network_difficulty()


        
        circulating_supply = self._calculate_supply(block_height) if block_height else 0
        remaining = 21_000_000 - circulating_supply
        
        return {
            "block_height": block_height,
            "hashrate_eh": hashrate / 1_000_000 if hashrate else None,
            "difficulty_t": difficulty / 1_000_000_000_000 if difficulty else None,
            "circulating_supply": circulating_supply,
            "remaining_supply": remaining,
            "percent_mined": (circulating_supply / 21_000_000) * 100 if circulating_supply else 0
        }

    @staticmethod
    def _calculate_supply(self, block_height: int) -> float:
        """Calcule le supply circulant basé sur la hauteur de bloc"""
        halving = block_height // 210000
        supply = 0
        reward = 50
        
        for _ in range(halving):
            supply += 210000 * reward
            reward /= 2
        
        supply += (block_height % 210000) * reward
        return supply