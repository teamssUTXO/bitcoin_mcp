from src.data.addresses_dataclasses import OverviewAddress, InfosAddress
from typing import Optional

from src.api.blockchain_client import BlockchainClient
from src.api.mempool_client import MempoolClient

class AddressAnalyzer:
    """Analyseur d'adresses Bitcoin"""

    def __init__(self):
        """
        Initialise l'analyseur d'adresses.
        """
        self.blockchain = BlockchainClient()
        self.mempool = MempoolClient()

    def get_address_info(self, address: str) -> Optional[str]:
        """
        Récupère les infos d'adresse depuis Mempool.space.

        Args:
            address: Adresse Bitcoin

        Returns:
            str: Infos formatées ou None en cas d'erreur
        """
        try:
            data = self.mempool.get_address_info(address)
            if not data:
                return None

            infos = InfosAddress.from_data(data)

            result = (
                f"=== Adresse Bitcoin ===\n"
                f"Adresse: {address}\n"
                f"Catégorie: {infos.category}\n"
                f"\n💰 BALANCE:\n"
                f"Confirmée: {infos.balance_btc:.8f} BTC\n"
                f"En attente: {infos.mempool_balance:,} sat\n"
                f"\n📊 ACTIVITÉ:\n"
                f"Status: {infos.status}\n"
                f"Total transactions: {infos.tx_count:,}\n"
                f"TX en mempool: {infos.mempool_tx_count}\n"
                f"Reçus: {infos.funded_txo_count:,} outputs ({infos.funded_txo_sum / 100_000_000:.8f} BTC)\n"
                f"Dépensés: {infos.spent_txo_count:,} outputs ({infos.spent_txo_sum / 100_000_000:.8f} BTC)"
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
            data = self.blockchain.get_address_info(address)
            if not data:
                return None

            infos = OverviewAddress.from_data(data)

            result = (
                f"=== Adresse Bitcoin ===\n"
                f"Adresse: {address}\n"
                f"\n💰 BALANCE:\n"
                f"Solde actuel: {infos.balance_btc:.8f} BTC\n"
                f"\n📊 HISTORIQUE:\n"
                f"Total reçu: {infos.received_btc:.8f} BTC\n"
                f"Total envoyé: {infos.sent_btc:.8f} BTC\n"
                f"Nombre de transactions: {infos.n_tx:,}"
            )
            return result

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None