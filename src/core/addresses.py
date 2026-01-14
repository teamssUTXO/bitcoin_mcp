from typing import Dict, Optional
from src.api.mempool_client import MempoolClient
from src.api.hiro_client import HiroClient


class AddressAnalyzer:
    def __init__(self):
        self.mempool = MempoolClient()
        self.hiro = HiroClient()
    
    def analyze_address(self, address: str) -> Dict:
        """Analyse complète d'une adresse Bitcoin"""
        stats = self.mempool.get_address_info(address)
        
        if not stats:
            return {"error": f"Could not retrieve data for {address}"}
        
        chain = stats.get('chain_stats', {})
        mempool = stats.get('mempool_stats', {})
        
        # Calculs balance
        balance_confirmed = (chain.get('funded_txo_sum', 0) - chain.get('spent_txo_sum', 0)) / 100_000_000
        balance_unconfirmed = (mempool.get('funded_txo_sum', 0) - mempool.get('spent_txo_sum', 0)) / 100_000_000
        total_balance = balance_confirmed + balance_unconfirmed
        
        total_received = chain.get('funded_txo_sum', 0) / 100_000_000
        total_spent = chain.get('spent_txo_sum', 0) / 100_000_000
        
        # Type d'adresse
        address_type = self._identify_address_type(address)
        
        # Assets Layer 2
        ordinals = self.hiro.get_ordinals(address)
        runes = self.hiro.get_runes(address)
        
        ordinals_count = ordinals.get('total', 0) if ordinals else 0
        runes_count = runes.get('total', 0) if runes else 0
        
        return {
            "address": address,
            "address_type": address_type,
            "balance_confirmed_btc": balance_confirmed,
            "balance_unconfirmed_btc": balance_unconfirmed,
            "balance_total_btc": total_balance,
            "total_received_btc": total_received,
            "total_spent_btc": total_spent,
            "tx_count": chain.get('tx_count', 0),
            "pending_tx_count": mempool.get('tx_count', 0),
            "utxo_count": chain.get('funded_txo_count', 0) - chain.get('spent_txo_count', 0),
            "ordinals_count": ordinals_count,
            "runes_count": runes_count,
            "has_assets": ordinals_count > 0 or runes_count > 0
        }
    
    def _identify_address_type(self, address: str) -> str:
        """Identifie le type d'adresse"""
        if address.startswith("bc1q"):
            return "SegWit (Bech32) - Native SegWit"
        elif address.startswith("bc1p"):
            return "Taproot (Bech32m) - Latest standard"
        elif address.startswith("3"):
            return "P2SH (Legacy SegWit wrapper)"
        elif address.startswith("1"):
            return "Legacy P2PKH (Old format)"
        return "Unknown"