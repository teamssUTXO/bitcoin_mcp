import logging
from typing import Optional

from src.api.mempool_client import get_mempool_client
from src.api.blockchain_client import get_blockchain_client

from data.network_dataclasses import DataNetworkFees, DataNetworkStats

from src.config import Config

logger = logging.getLogger(__name__)

class NetworkAnalyzer:
    """Bitcoin Network Analyzer"""

    def __init__(self):
        """
        Initialize Bitcoin Network Analyzer.
        """
        self.mempool = get_mempool_client()
        self.blockchain = get_blockchain_client()

    def get_network_stats(self) -> Optional[str]:
        """
        Retrieves current recommended Bitcoin transaction fees.

        Returns:
            A Markdown formatted string including:
            - Fee rates (sat/vB) for different priority levels (Fast, Half-hour, Standard, Economy).
            - Estimated total cost in BTC for a standard transaction (250 vBytes).
            Returns None if an API error occurs or data is missing.
        """
        try:
            data: dict = self.blockchain.get_network_stats()
            if not data:
                return None

            infos: DataNetworkStats = DataNetworkStats.from_data(data)

            result: str = (
                f"## Bitcoin Network Statistics\n"
                f"Market Price: ${infos.market_price_usd:,.2f}\n"
                f"Hashrate: {infos.hash_rate / 1_000_000_000_000:.2f} TH/s\n"
                f"Difficulty: {infos.difficulty:.0f}\n"
                f"Next Adjustment: Block {infos.nextretarget}\n\n"
                f"## Block Metrics\n"
                f"Blocks Mined (24h): {infos.n_blocks_mined}\n"
                f"Total Blocks: {infos.n_blocks_total}\n"
                f"Avg Block Time: {infos.minutes_between_blocks:.2f} min\n"
                f"Avg Block Size: {infos.blocks_size} bytes\n\n"
                f"## Transaction Activity\n"
                f"Transactions (24h): {infos.n_tx}\n"
                f"Estimated BTC Sent: {infos.estimated_btc_sent:.2f} BTC\n"
                f"Transaction Volume: ${infos.estimated_transaction_volume_usd:.0f}\n\n"
                f"## Mining Economics\n"
                f"BTC Mined (24h): {infos.n_btc_mined / 100_000_000:.2f} BTC\n"
                f"Total Fees: {infos.total_fees_btc / 100_000_000:.8f} BTC\n"
                f"Miner Revenue: {infos.miners_revenue_btc:.2f} BTC | ${infos.miners_revenues_usd:.0f}\n\n"
                f"## Supply Information\n"
                f"Circulating Supply: {infos.totalbc:.2f} BTC"
            )
            return result

        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None


    def get_network_recommended_fees(self) -> Optional[str]:
        """
        Retrieves current recommended Bitcoin transaction fees.

        Returns:
            A Markdown formatted string including:
            - Fee rates (sat/vB) for different priority levels (Fast, Half-hour, Standard, Economy).
            - Estimated total cost in BTC for a standard transaction (250 vBytes).
            Returns None if an API error occurs or data is missing.
        """
        try:
            data: dict = self.mempool.get_recommended_fees()
            if not data:
                return None

            tx_size: int = 250 # taille de transaction standard
            infos: DataNetworkFees = DataNetworkFees.from_data(data)

            costs: dict = {
                'Rapide (~10 min)': (infos.fastest * tx_size) / Config.SATOSHI,
                'Demi-heure': (infos.half_hour * tx_size) / Config.SATOSHI,
                'Standard (~1h)': (infos.hour * tx_size) / Config.SATOSHI,
                'Économique': (infos.economy * tx_size) / Config.SATOSHI
            }

            result: str = (
                f"## Recommended Transaction Fees\n"
                f"Fastest (~10 min): {infos.fastest} sat/vB | Cost: ~{list(costs.values())[0]} BTC\n"
                f"Half-Hour (~30 min): {infos.half_hour} sat/vB | Cost: ~{list(costs.values())[1]} BTC\n"
                f"Standard (~60 min): {infos.hour} sat/vB | Cost: ~{list(costs.values())[2]} BTC\n"
                f"Economy: {infos.economy} sat/vB | Cost: ~{list(costs.values())[3]} BTC\n"
            )

            return result

        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None


    def get_network_health(self) -> Optional[str]:
        """
        Evaluates the overall health and stability of the Bitcoin network.

        Returns:
            A formatted string including:
            - A health score (0-100) and status (Excellent, Good, Fair, Poor).
            - A list of detected issues (e.g., block time anomalies, low hashrate).
            - A confirmation message if no issues are detected.
            Returns None if an API error occurs or data is missing.
        """
        try:
            data: dict = self.blockchain.get_network_stats()
            if not data:
                return None

            infos: DataNetworkStats = DataNetworkStats.from_data(data)

            health_score: int = 100
            issues: list = []

            if infos.minutes_between_blocks > 15:
                health_score -= 20
                issues.append(f"Slow blocks ({infos.minutes_between_blocks:.1f} min)")
            elif infos.minutes_between_blocks < 5:
                health_score -= 10
                issues.append(f"Fast blocks ({infos.minutes_between_blocks:.1f} min)")

            if infos.hash_rate < 100_000_000_000:  # < 100 TH/s
                health_score -= 30
                issues.append("Low hashrate")

            if infos.n_tx < 100_000:
                health_score -= 15
                issues.append("Low transaction volume")

            status: str = "Excellent" if health_score >= 90 else \
                "Good" if health_score >= 70 else \
                    "Fair" if health_score >= 50 else "Poor"

            result: str = f"Network Status: {status} ({health_score}/100)\n"
            if issues:
                result += "Issues: " + ", ".join(issues)
            else:
                result += "No issues detected"

            return result

        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None


# Singleton instance for the analyzer
_network_analyser_instance = None

def get_network_analyser_client() -> NetworkAnalyzer:
    """Get or create the Network Analyzer client singleton instance."""
    global _network_analyser_instance
    if _network_analyser_instance is None:
        _network_analyser_instance = NetworkAnalyzer()
    return _network_analyser_instance