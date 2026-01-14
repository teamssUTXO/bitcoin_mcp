from typing import Dict, Optional
from src.api.mempool_client import MempoolClient
from src.api.blockchain_client import BlockchainClient


class MiningAnalyzer:
    def __init__(self):
        self.mempool = MempoolClient()
        self.blockchain = BlockchainClient()
    
    def get_mining_statistics(self) -> Dict:
        """Statistiques complètes de mining"""
        hashrate = self.blockchain.get_hashrate()
        difficulty = self.blockchain.get_difficulty()
        tip_height = self.mempool.get_block_tip_height()
        
        # Calcul next halving
        next_halving_data = self._calculate_next_halving(tip_height) if tip_height else {}
        
        # Block timing
        block_timing = self._analyze_block_timing()
        
        return {
            "hashrate_eh": hashrate / 1_000_000 if hashrate else None,
            "hashrate_th": hashrate / 1_000_000 * 1_000_000 if hashrate else None,
            "difficulty_t": difficulty / 1_000_000_000_000 if difficulty else None,
            "current_block_height": tip_height,
            **next_halving_data,
            **block_timing
        }
    
    def _calculate_next_halving(self, tip_height: int) -> Dict:
        """Calcule les données du prochain halving"""
        next_halving = 210000 * ((tip_height // 210000) + 1)
        blocks_to_halving = next_halving - tip_height
        days_to_halving = (blocks_to_halving * 10) / (60 * 24)
        
        current_reward = 6.25 if tip_height < 840000 else 3.125
        
        return {
            "current_block_reward_btc": current_reward,
            "next_halving_block": next_halving,
            "blocks_to_halving": blocks_to_halving,
            "days_to_halving": int(days_to_halving)
        }
    
    def _analyze_block_timing(self) -> Dict:
        """Analyse le timing des blocs récents"""
        blocks = self.mempool.get_recent_blocks()
        
        if not blocks or len(blocks) < 10:
            return {"avg_block_time_min": None, "timing_status": "Unknown"}
        
        times = []
        for i in range(1, min(10, len(blocks))):
            time_diff = (blocks[i-1]['timestamp'] - blocks[i]['timestamp']) / 60
            times.append(time_diff)
        
        avg_time = sum(times) / len(times) if times else 10
        
        if 9 <= avg_time <= 11:
            status = "ON TARGET"
        elif avg_time > 11:
            status = "SLOWER"
        else:
            status = "FASTER"
        
        return {
            "avg_block_time_min": round(avg_time, 1),
            "target_block_time_min": 10.0,
            "timing_status": status
        }