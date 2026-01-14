from typing import Dict, Optional
from src.api.mempool_client import MempoolClient
from src.api.coingecko_client import CoinGeckoClient


class TransactionAnalyzer:
    def __init__(self):
        self.mempool = MempoolClient()
        self.coingecko = CoinGeckoClient()
    
    def get_fee_analysis(self) -> Dict:
        """Analyse complète des frais de transaction"""
        fees = self.mempool.get_recommended_fees()
        mempool_info = self.mempool.get_mempool_info()
        btc_price = self.coingecko.get_bitcoin_price()
        
        if not fees:
            return {"error": "Fee data unavailable"}
        
        # Calcul coût en USD pour tx typique (250 vBytes)
        typical_size = 250
        costs_usd = {}
        
        if btc_price:
            for priority, sat_vb in fees.items():
                sats = sat_vb * typical_size
                btc = sats / 100_000_000
                costs_usd[priority] = btc * btc_price
        
        # Niveau de congestion
        congestion = "NORMAL"
        if mempool_info:
            vbytes = mempool_info.get('vBytes', 0)
            if vbytes > 100_000_000:
                congestion = "SEVERE"
            elif vbytes > 50_000_000:
                congestion = "MODERATE"
        
        return {
            "fee_rates": fees,
            "costs_usd": costs_usd,
            "typical_tx_size_vbytes": typical_size,
            "congestion_level": congestion,
            "mempool_size_mb": mempool_info.get('vBytes', 0) / 1_000_000 if mempool_info else None,
            "pending_tx_count": mempool_info.get('count', 0) if mempool_info else None
        }
    
    def get_transaction_details(self, txid: str) -> Dict:
        """Récupère les détails d'une transaction"""
        tx = self.mempool.get_transaction(txid)
        
        if not tx:
            return {"error": f"Transaction {txid} not found"}
        
        # Vérifier confirmation
        is_confirmed = 'status' in tx and tx['status'].get('confirmed', False)
        
        if is_confirmed:
            block_height = tx['status']['block_height']
            tip_height = self.mempool.get_block_tip_height()
            confirmations = tip_height - block_height + 1 if tip_height else 0
        else:
            confirmations = 0
        
        # Calculs
        fee_sats = tx.get('fee', 0)
        vsize = tx.get('vsize', tx.get('size', 0))
        fee_rate = (fee_sats / vsize) if vsize > 0 else 0
        
        # RBF detection
        rbf_enabled = any(
            inp.get('sequence', 0xffffffff) < 0xfffffffe 
            for inp in tx.get('vin', [])
        )
        
        return {
            "txid": txid,
            "is_confirmed": is_confirmed,
            "confirmations": confirmations,
            "block_height": tx['status'].get('block_height') if is_confirmed else None,
            "fee_sats": fee_sats,
            "fee_rate_sat_vb": fee_rate,
            "size_bytes": tx.get('size', 0),
            "vsize_vbytes": vsize,
            "weight": tx.get('weight', 0),
            "inputs_count": len(tx.get('vin', [])),
            "outputs_count": len(tx.get('vout', [])),
            "rbf_enabled": rbf_enabled
        }