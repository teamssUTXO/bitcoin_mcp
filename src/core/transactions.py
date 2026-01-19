from typing import Optional

from data.transactions_dataclasses import TransactionsAddress
from src.api.mempool_client import get_mempool_client
from src.api.blockchain_client import get_blockchain_client
from src.data.transactions_dataclasses import TransactionInfo, TxInOut


# TODO : remplacer les calculs dans post_init par @property
class TransactionAnalyzer:
    """Analyseur de transactions Bitcoin"""

    def __init__(self):
        """
        Initialise l'analyseur de transactions.
        """
        self.mempool = get_mempool_client()
        self.blockchain = get_blockchain_client()

    def get_tx_info(self, txid: str) -> Optional[str]:
        """
        Récupère les informations détaillées sur une transaction.

        Args:
            txid: Identifiant de la transaction

        Returns:
            str: Infos de transaction formatées ou None en cas d'erreur
        """
        try:
            data: dict = self.mempool.get_tx_info(txid)
            if not data:
                return None

            infos: TransactionInfo = TransactionInfo.from_data(data)

            #TODO : Faire le rapport par IA
            result: str = (""
                # f"=== Transaction ===\n"
                # f"TXID: {txid}\n"
                # f"Status: {infos.confirmed}\n"
                # f"Bloc: #{infos.infosblock_height} | {infos.block_hash} | {infos.date_str}\n"
                # f"\n=== Détails ===\n"
                # f"Taille: {infos.size} bytes | Weight: {infos.weight}\n"
                # f"Inputs: {infos.vin_count} | Outputs: {infos.vout_count}\n"
                # f"Montant total: {infos.total_output_btc:.8f} BTC\n"
                # f"Frais: {infos.fee:,} sat ({infos.fee_rate:.2f} sat/vB)\n"
                # f"Version: {infos.version} | Locktime: {infos.locktime}"
            )
            return result

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


    def get_tx_inputs_outputs(self, txid: str) -> Optional[str]:
        """
        Récupère les détails des inputs et outputs d'une transaction.

        Args:
            txid: Identifiant de la transaction

        Returns:
            str: Détails inputs/outputs ou None en cas d'erreur
        """
        try:
            data: dict = self.mempool.get_tx_info(txid)
            if not data:
                return None

            infos: TxInOut = TxInOut.from_data(data)

            # TODO : Faire le rapport par IA
            result: str = (""
                # f"=== Transaction ===\n"
                # f"TXID: {txid}\n"
                # f"Status: {infos.confirmed}\n"
                # f"Bloc: #{infos.infosblock_height} | {infos.block_hash} | {infos.date_str}\n"
                # f"\n=== Détails ===\n"
                # f"Taille: {infos.size} bytes | Weight: {infos.weight}\n"
                # f"Inputs: {infos.vin_count} | Outputs: {infos.vout_count}\n"
                # f"Montant total: {infos.total_output_btc:.8f} BTC\n"
                # f"Frais: {infos.fee:,} sat ({infos.fee_rate:.2f} sat/vB)\n"
                # f"Version: {infos.version} | Locktime: {infos.locktime}"
            )
            return result

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


    def get_address_transactions(self, address: str) -> Optional[str]:
        """
        Récupère les transactions d'une addresse

        Args:
            address: Adresse Bitcoin

        Returns:
            str: Renvoie les id des transactions de l'adresse
        """
        try:
            data: dict = self.blockchain.get_address_info(address)
            if not data:
                return None

            infos: TransactionsAddress = TransactionsAddress.from_data(data)

            result: str = ""
            for i in range(infos.len_txs):
                result += f"TXID : {infos.txs_hash[i]}\n"
                result += f"Date : {infos.txs_date[i]}\n"
                result += f"Montant envoyé : {infos.amount_sent[i]} sats\n"
                result += "Destinations :\n"

                for addr, value in infos.destinations[i]:
                    result += f"  → {addr} : {value} sats\n"
                result += "\n"

            return result


        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None