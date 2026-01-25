import logging
from typing import Optional
from src.api.blockchain_client import get_blockchain_client
from src.api.mempool_client import get_mempool_client
from src.data.addresses_dataclasses import DataOverviewAddress, DataInfosAddress
from src.config import Config


logger = logging.getLogger(__name__)

class AddressAnalyzer:
    """Bitcoin Address Analyzer"""

    def __init__(self):
        """
        Initialize Addresses Analyzer.
        """
        self.blockchain = get_blockchain_client()
        self.mempool = get_mempool_client()

    def get_address_info(self, address: str) -> Optional[str]:
        """
        Retrieves a complete summary of a Bitcoin address.

        Args:
            address: The Bitcoin address to analyze.

        Returns:
            A Markdown formatted string including:
            - Balance category (Large, Medium, Low, Cleared).
            - Activity status (Active, Sleeping, Inactive).
            - Confirmed balance (BTC) and pending mempool balance (sat).
            - Transaction counts and output history.
            Returns None if an API error occurs or the address is not found.
        """
        try:
            data: dict = self.mempool.get_address_info(address)
            if not data:
                return None

            infos: DataInfosAddress = DataInfosAddress.from_data(data)

            funded_txo_sum: int = infos.chain_stats.get("funded_txo_sum")
            spent_txo_sum: int = infos.chain_stats.get('spent_txo_sum')

            balance_btc: float = (funded_txo_sum - spent_txo_sum) / Config.SATOSHI

            tx_count: int = infos.chain_stats.get('tx_count')
            funded_txo_count: int = infos.chain_stats.get('funded_txo_count')
            spent_txo_count: int = infos.chain_stats.get('spent_txo_count')

            mempool_balance: int = infos.mempool_stats.get('funded_txo_sum') - infos.mempool_stats.get('spent_txo_sum')
            mempool_tx_count: int = infos.mempool_stats.get('tx_count')

            if balance_btc == 0 and tx_count > 0:
                category: str = "Cleared address"
            elif balance_btc > 1:  # > 1 BTC
                category: str = "Large Balance (> 1 BTC)"
            elif balance_btc > 0.1:  # > 0.1 BTC
                category: str = "Medium Balance (average)"
            elif balance_btc > 0:
                category: str = "Low Balance (< 0.1 BTC)"
            else:
                category: str = "Empty address"

            if mempool_tx_count > 0:
                status: str = "ACTIVE - Transactions in progress"
            elif balance_btc > 0:
                status: str = "SLEEPING - Existing balance, no recent TX"
            else:
                status: str = "INACTIVE - Empty balance"

            result: str = (
                f"## Bitcoin Address Analysis\n"
                f"Address: {address}\n"
                f"Category: {category}\n"
                f"Status: {status}\n\n"
                f"## Balance\n"
                f"Confirmed: {balance_btc:.8f} BTC\n"
                f"Mempool: {mempool_balance} sat\n\n"
                f"## Transaction Activity\n"
                f"Total: {tx_count}\n"
                f"Mempool: {mempool_tx_count}\n\n"
                f"## Outputs\n"
                f"Received: {funded_txo_count} outputs | {funded_txo_sum / 100_000_000:.8f} BTC\n"
                f"Spent: {spent_txo_count} outputs | {spent_txo_sum / 100_000_000:.8f} BTC"
            )
            return result

        except Exception as e:
            logger.error(f"Failed to process: {e}", extra={"address": address}, exc_info=True)
            return None

    def get_address_info_overview(self, address: str) -> Optional[str]:
        """
        Retrieves a high-level overview of a Bitcoin address.

        Args:
            address: The Bitcoin address to analyze (base58 or hash160).

        Returns:
            A Markdown formatted string including:
            - Current balance in BTC.
            - Historical activity (Total received and sent in BTC).
            - Total number of transactions.
            Returns None if an API error occurs or data is missing.
        """
        try:
            data: dict = self.blockchain.get_address_info(address)
            if not data:
                return None

            infos: DataOverviewAddress = DataOverviewAddress.from_data(data)

            balance_btc: float = infos.final_balance / Config.SATOSHI
            received_btc: float = infos.total_received / Config.SATOSHI
            sent_btc: float = infos.total_sent / Config.SATOSHI

            result: str = (
                f"## Bitcoin Address Overview\n"
                f"Address: {address}\n\n"
                f"## Balance\n"
                f"Current: {balance_btc:.8f} BTC\n\n"
                f"## Historical Activity\n"
                f"Total Received: {received_btc:.8f} BTC\n"
                f"Total Sent: {sent_btc:.8f} BTC\n"
                f"Transactions: {infos.n_tx}"
            )
            return result


        except Exception as e:
            logger.error(f"Failed to process: {e}", extra={"address": address}, exc_info=True)
            return None


# Singleton instance for the analyzer
_addresses_analyser_instance = None

def get_addresses_analyser_client() -> AddressAnalyzer:
    """Get or create the Addresses Analyzer client singleton instance."""
    global _addresses_analyser_instance
    if _addresses_analyser_instance is None:
        _addresses_analyser_instance = AddressAnalyzer()
    return _addresses_analyser_instance