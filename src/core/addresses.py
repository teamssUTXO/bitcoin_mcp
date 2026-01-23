from typing import Optional

from src.api.blockchain_client import get_blockchain_client
from src.api.mempool_client import get_mempool_client

from src.data.addresses_dataclasses import DataOverviewAddress, DataInfosAddress

from src.config import Config


class AddressAnalyzer:
    """Analyseur d'adresses Bitcoin"""

    def __init__(self):
        """
        Initialise l'analyseur d'adresses.
        """
        self.blockchain = get_blockchain_client()
        self.mempool = get_mempool_client()

    def get_address_info(self, address: str) -> Optional[str]:
        """
        Récupère les infos d'adresse depuis Mempool.space.

        Args:
            address: Adresse Bitcoin

        Returns:
            str: Infos formatées ou None en cas d'erreur
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
                category: str = "Adresse vidée"
            elif balance_btc > 1:  # > 1 BTC
                category: str = "Grande balance (> 1 BTC)"
            elif balance_btc > 0.1:  # > 0.1 BTC
                category: str = "Balance moyenne"
            elif balance_btc > 0:
                category: str = "Petite balance (< 0.1 BTC)"
            else:
                category: str = "Adresse vide"

            if mempool_tx_count > 0:
                status: str = "ACTIVE - Transactions en cours"
            elif balance_btc > 0:
                status: str = "DORMANTE - Balance existante, aucune TX récente"
            else:
                status: str = "INACTIVE - Balance nulle"

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

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_address_info_overview(self, address: str) -> Optional[str]:
        """
        Récupère les infos d'adresse depuis Blockchain.com.

        Args:
            address: Adresse Bitcoin en base58 ou hash160

        Returns:
            str: Infos formatées ou None en cas d'erreur
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

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


# Singleton instance for the analyzer
_addresses_analyser_instance = None

def get_addresses_analyser_client() -> AddressAnalyzer:
    """Get or create the Addresses Analyzer client singleton instance."""
    global _addresses_analyser_instance
    if _addresses_analyser_instance is None:
        _addresses_analyser_instance = AddressAnalyzer()
    return _addresses_analyser_instance