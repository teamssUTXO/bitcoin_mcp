from typing import Optional

from src.api.blockchain_client import get_blockchain_client
from src.api.mempool_client import get_mempool_client

from src.data.addresses_dataclasses import OverviewAddress, InfosAddress

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

            infos: InfosAddress = InfosAddress.from_data(data)

            funded_txo_sum = infos.chain_stats["funded_txo_sum"]
            spent_txo_sum = infos.chain_stats['spent_txo_sum']

            balance_btc = (funded_txo_sum - spent_txo_sum) / Config.SATOSHI

            tx_count = infos.chain_stats['tx_count']
            funded_txo_count = infos.chain_stats['funded_txo_count']
            spent_txo_count = infos.chain_stats['spent_txo_count']

            mempool_balance = infos.mempool_stats['funded_txo_sum'] - infos.mempool_stats['spent_txo_sum']
            mempool_tx_count = infos.mempool_stats['tx_count']

            if balance_btc == 0 and tx_count > 0:
                category = "Adresse vidée"
            elif balance_btc > 1:  # > 1 BTC
                category = "Grande balance (> 1 BTC)"
            elif balance_btc > 0.1:  # > 0.1 BTC
                category = "Balance moyenne"
            elif balance_btc > 0:
                category = "Petite balance (< 0.1 BTC)"
            else:
                category = "Adresse vide"

            if mempool_tx_count > 0:
                status = "ACTIVE - Transactions en cours"
            elif balance_btc > 0:
                status = "DORMANTE - Balance existante, aucune TX récente"
            else:
                status = "INACTIVE - Balance nulle"

            result: str = (
                f"=== Adresse Bitcoin ===\n"
                f"Adresse: {address}\n"
                f"Catégorie: {category}\n"
                f"\n💰 BALANCE:\n"
                f"Confirmée: {balance_btc:.8f} BTC\n"
                f"En attente: {mempool_balance:,} sat\n"
                f"\n📊 ACTIVITÉ:\n"
                f"Status: {status}\n"
                f"Total transactions: {tx_count:,}\n"
                f"TX en mempool: {mempool_tx_count}\n"
                f"Reçus: {funded_txo_count:,} outputs ({funded_txo_sum / 100_000_000:.8f} BTC)\n"
                f"Dépensés: {spent_txo_count:,} outputs ({spent_txo_sum / 100_000_000:.8f} BTC)"
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

            infos: OverviewAddress = OverviewAddress.from_data(data)

            balance_btc = infos.final_balance / Config.SATOSHI
            received_btc = infos.total_received / Config.SATOSHI
            sent_btc = infos.total_sent / Config.SATOSHI
            # self.txs = [
            #     {
            #         "hash": tx.get("hash"),
            #         "time": tx.get("time"),
            #         "result": tx.get("result", 0),
            #         "fee": tx.get("fee", 0),
            #     }
            #     for tx in self.txs
            # ]

            result: str = (
                f"=== Adresse Bitcoin ===\n"
                f"Adresse: {address}\n"
                f"\n💰 BALANCE:\n"
                f"Solde actuel: {balance_btc:.8f} BTC\n"
                f"\n📊 HISTORIQUE:\n"
                f"Total reçu: {received_btc:.8f} BTC\n"
                f"Total envoyé: {sent_btc:.8f} BTC\n"
                f"Nombre de transactions: {infos.n_tx:,}"
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