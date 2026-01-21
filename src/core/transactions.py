from typing import Optional
from datetime import datetime

from src.api.mempool_client import get_mempool_client
from src.api.blockchain_client import get_blockchain_client

from src.data.transactions_dataclasses import DataTransactionInfo, DataTxInOut, DataTxOutput, DataTxInput
from src.data.transactions_dataclasses import DataTransactionsAddress

from src.config import Config


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

            infos: DataTransactionInfo = DataTransactionInfo.from_data(data)

            nb_inputs: int = len(infos.vin)
            nb_outputs: int = len(infos.vout)

            fee_btc: float = infos.fee / Config.SATOSHI

            transaction_status: str = "COMFIRMED" if infos.status.get("confirmed") else "UNCOMFIRMED"
            transaction_block_time: int = infos.status.get('block_time', 0)
            transaction_block_hash: str = infos.status.get('block_hash', '')
            transaction_block_height: int = infos.status.get('block_height', 0)

            date_str: str = datetime.fromtimestamp(transaction_block_time).strftime(
                '%Y-%m-%d %H:%M:%S') if transaction_block_time else 'Non confirmée'

            total_sats_out: int = sum(out.get('value', 0) for out in infos.vout)
            total_btc_out: float = total_sats_out / Config.SATOSHI

            sat_per_byte: int = infos.fee / infos.size if infos.size > 0 else 0

            status_icon: str = "✅" if infos.status.get("confirmed") else "⏳"

            result: str = (
                f"=== Transaction {status_icon} ===\n"
                f"Statut: {transaction_status}\n"
                f"Date: {date_str}\n"
                f"\n"
                f"--- Économie & Flux ---\n"
                f"Montant Total: {total_btc_out:,.8f} BTC\n"
                f"Frais payés: {fee_btc:,.8f} BTC\n"
                f"Taux de frais: {sat_per_byte:.2f} sat/vB\n"
                f"\n"
                f"--- Structure Technique ---\n"
                f"Taille: {infos.size:,} bytes\n"
                f"Entrées (Inputs): {nb_inputs}\n"
                f"Sorties (Outputs): {nb_outputs}\n"
                f"\n"
                f"--- Informations du Bloc ---\n"
                f"Hauteur (Height): {transaction_block_height:,}\n"
                f"Hash du bloc: {transaction_block_hash}\n"
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

            infos: DataTxInOut = DataTxInOut.from_data(data)

            inputs: list[DataTxInput] = [DataTxInput.from_data(v) for v in infos.vin]
            outputs: list[DataTxOutput] = [DataTxOutput.from_data(v) for v in infos.vout]

            total_input_sats: int = sum(i.value for i in inputs)
            total_output_sats: int = sum(o.value for o in outputs)

            total_input_btc: float = total_input_sats / Config.SATOSHI
            total_output_btc: float = total_output_sats / Config.SATOSHI

            addresses_in: list = [i.address for i in inputs]
            addresses_out: list = [o.address for o in outputs]

            fee_network: float = total_input_btc - total_output_btc

            detailed_in_lines: list = []
            for i in inputs:
                addr: str = i.address if i.address else "SYSTEM (Coinbase/Mint)"
                val: float = i.value / Config.SATOSHI
                detailed_in_lines.append(f"  [IN]  {val:12.8f} BTC | Depuis: {addr}")

            detailed_out_lines: list = []
            for o in outputs:
                addr: str = o.address if o.address else "DATA (OP_RETURN)"
                val: float = o.value / Config.SATOSHI
                detailed_out_lines.append(f"  [OUT] {val:12.8f} BTC | Vers:   {addr}")

            clean_in_addrs: list = [a for a in addresses_in if a]
            clean_out_addrs: list = [a for a in addresses_out if a]

            list_in_txt: str = "\n".join([f"  - {a}" for a in clean_in_addrs]) if clean_in_addrs else "  - Aucune adresse publique (Coinbase)"
            list_out_txt: str = "\n".join([f"  - {a}" for a in clean_out_addrs]) if clean_out_addrs else "  - Aucune adresse standard"

            result: str = (
                f"=== Analyse Complète de la Transaction ===\n"
                f"--- Bilan Comptable ---\n"
                f"Volume Entrant: {total_input_btc:,.8f} BTC\n"
                f"Volume Sortant: {total_output_btc:,.8f} BTC\n"
                f"Frais Réseau:   {fee_network:,.8f} BTC\n"
                f"\n"
                f"--- Flux Détaillé (UTXO) ---\n"
                f"Mouvements Entrants :\n"
                f"{chr(10).join(detailed_in_lines)}\n"
                f"\n"
                f"Mouvements Sortants :\n"
                f"{chr(10).join(detailed_out_lines)}\n"
                f"\n"
                f"--- Carnet des Participants ---\n"
                f"Liste des expéditeurs ({len(clean_in_addrs)}) :\n"
                f"{list_in_txt}\n"
                f"\n"
                f"Liste des destinataires ({len(clean_out_addrs)}) :\n"
                f"{list_out_txt}\n"
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

            infos: DataTransactionsAddress = DataTransactionsAddress.from_data(data)

            len_txs: int = len(infos.txs)

            txs_hash: list = [tx["hash"] for tx in infos.txs]
            txs_date: list = [datetime.fromtimestamp(tx["time"]) for tx in infos.txs]

            amount_sent: list = [
                sum(
                    vin.get("prev_out", {}).get("value", 0)
                    for vin in tx.get("inputs", [])
                    if vin.get("prev_out", {}).get("addr") == address
                )
                for tx in infos.txs
            ]

            # Destinations (adresse + montant)
            # Enlevé car trop de tokens
            # destinations: list = [
            #     [
            #         (o.get("addr", ""), o.get("value", 0))
            #         for o in tx.get("out", [])
            #     ]
            #     for tx in infos.txs
            # ]

            result: str = ""
            for i in range(len_txs):
                result += f"TXID : {txs_hash[i]}\n"
                result += f"Date : {txs_date[i]}\n"
                result += f"Montant envoyé : {amount_sent[i]} sats\n"
                # result += "Destinations :\n"

                # for addr, value in destinations[i]:
                #     result += f"  → {addr} : {value} sats\n"
                # result += "\n"

            return result


        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


# Singleton instance for the analyzer
_transactions_analyser_instance = None

def get_transactions_analyser_client() -> TransactionAnalyzer:
    """Get or create the Transactions Analyzer client singleton instance."""
    global _transactions_analyser_instance
    if _transactions_analyser_instance is None:
        _transactions_analyser_instance = TransactionAnalyzer()
    return _transactions_analyser_instance