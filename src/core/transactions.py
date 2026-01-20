from typing import Optional
from datetime import datetime

from data.transactions_dataclasses import TransactionsAddress
from src.api.mempool_client import get_mempool_client
from src.api.blockchain_client import get_blockchain_client
from src.data.transactions_dataclasses import TransactionInfo, TxInOut, TxOutput, TxInput

from src.config import Config


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

            nb_inputs = len(infos.vin)
            nb_outputs = len(infos.vout)

            fee_btc = infos.fee / Config.SATOSHI

            fee_rate = fee_btc / infos.size if infos.size > 0 else 0

            transaction_status = ("COMFIRMED" if infos.status.get("confirmed") else "UNCOMFIRMED")
            transaction_block_time = infos.status.get('block_time', 0)
            transaction_block_hash = infos.status.get('block_hash', '')
            transaction_block_height = infos.status.get('block_height', 0)

            date_str = datetime.fromtimestamp(transaction_block_time).strftime(
                '%Y-%m-%d %H:%M:%S') if transaction_block_time else 'Non confirmée'

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

            inputs = [TxInput.from_data(v) for v in infos.vin]
            outputs = [TxOutput.from_data(v) for v in infos.vout]

            total_input_sats: int = sum(i.value for i in inputs)
            total_output_sats: int = sum(o.value for o in outputs)

            total_input_btc: float = total_input_sats / Config.SATOSHI
            total_output_btc: float = total_output_sats / Config.SATOSHI

            addresses_in: list = [i.address for i in inputs]
            addresses_out: list = [o.address for o in outputs]

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

            len_txs = len(infos.txs)

            txs_hash = [tx["hash"] for tx in infos.txs]
            txs_date = [datetime.fromtimestamp(tx["time"]) for tx in infos.txs]

            amount_sent = [
                sum(
                    vin.get("prev_out", {}).get("value", 0)
                    for vin in tx.get("inputs", [])
                    if vin.get("prev_out", {}).get("addr") == address
                )
                for tx in infos.txs
            ]

            # Destinations (adresse + montant)
            destinations = [
                [
                    (o.get("addr", ""), o.get("value", 0))
                    for o in tx.get("out", [])
                ]
                for tx in infos.txs
            ]

            result: str = ""
            for i in range(len_txs):
                result += f"TXID : {txs_hash[i]}\n"
                result += f"Date : {txs_date[i]}\n"
                result += f"Montant envoyé : {amount_sent[i]} sats\n"
                result += "Destinations :\n"

                for addr, value in destinations[i]:
                    result += f"  → {addr} : {value} sats\n"
                result += "\n"

            return result


        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None