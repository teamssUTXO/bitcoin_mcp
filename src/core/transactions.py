import logging
from typing import Optional
from datetime import datetime

from src.api.mempool_client import get_mempool_client
from src.api.blockchain_client import get_blockchain_client

from src.data.transactions_dataclasses import DataTransactionInfo, DataTxInOut, DataTxOutput, DataTxInput
from src.data.transactions_dataclasses import DataTransactionsAddress

from src.config import Config


logger = logging.getLogger(__name__)

class TransactionAnalyzer:
    """Bitcoin Transactions Analyzer"""

    def __init__(self):
        """
        Initialize Bitcoin Transactions Analyzer.
        """
        self.mempool = get_mempool_client()
        self.blockchain = get_blockchain_client()

    def get_tx_info(self, txid: str) -> Optional[str]:
        """
        Retrieves detailed information for a specific Bitcoin transaction.

        Args:
            txid: The unique transaction ID (hash) to inspect.

        Returns:
            A Markdown formatted string including:
            - Confirmation status (Confirmed/Unconfirmed) and timestamp.
            - Economic flow (Total BTC amount, fees paid, and fee rate in sat/vB).
            - Technical structure (Size in bytes, number of inputs and outputs).
            - Block information (Height and block hash if confirmed).
            Returns None if the transaction is not found or an API error occurs.
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
                f"## Transaction {status_icon}\n"
                f"Status: {transaction_status}\n"
                f"Date: {date_str}\n\n"
                f"## Economics & Flow\n"
                f"Total Amount: {total_btc_out:.8f} BTC\n"
                f"Fees Paid: {fee_btc:.8f} BTC\n"
                f"Fee Rate: {sat_per_byte:.2f} sat/vB\n\n"
                f"## Technical Structure\n"
                f"Size: {infos.size} bytes\n"
                f"Inputs: {nb_inputs}\n"
                f"Outputs: {nb_outputs}\n\n"
                f"## Block Information\n"
                f"Block Height: {transaction_block_height}\n"
                f"Block Hash: {transaction_block_hash}\n"
            )

            return result


        except Exception as e:
            logger.error(f"Failed to process: {e}", extra={"txid": txid}, exc_info=True)
            return None


    def get_tx_inputs_outputs(self, txid: str) -> Optional[str]:
        """
        Retrieves the detailed input and output flow of a transaction.

        Args:
            txid: The unique transaction ID (hash) to analyze.

        Returns:
            A Markdown formatted string including:
            - Accounting summary (Total Input vs Output and Network Fees).
            - Detailed UTXO flow (BTC amounts mapped to specific addresses).
            - Participant registry (List of all sender and recipient addresses).
            Returns None if the transaction is not found or an API error occurs.
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
                f"## Transaction Flow Analysis\n"
                f"## Accounting Summary\n"
                f"Total Input: {total_input_btc:.8f} BTC\n"
                f"Total Output: {total_output_btc:.8f} BTC\n"
                f"Network Fees: {fee_network:.8f} BTC\n\n"
                f"## UTXO Flow Details\n"
                f"Inputs:\n"
                f"{chr(10).join(detailed_in_lines)}\n\n"
                f"Outputs:\n"
                f"{chr(10).join(detailed_out_lines)}\n\n"
                f"## Participant Registry\n"
                f"Senders ({len(clean_in_addrs)}):\n"
                f"{list_in_txt}\n\n"
                f"Recipients ({len(clean_out_addrs)}):\n"
                f"{list_out_txt}\n"
            )

            return result

        except Exception as e:
            logger.error(f"Failed to process: {e}", extra={"txid": txid}, exc_info=True)
            return None


    def get_address_transactions(self, address: str) -> Optional[str]:
        """
        Retrieves the transaction history for a specific Bitcoin address.

        Args:
            address: The Bitcoin address to query.

        Returns:
            A formatted string listing recent transactions, including:
            - Transaction ID (TXID).
            - Confirmation date and time.
            - The specific amount sent by this address in each transaction (sats).
            Returns None if the address has no history or an API error occurs.
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
                result += f"TXID: {txs_hash[i]}\n"
                result += f"Date: {txs_date[i]}\n"
                result += f"Amount: {amount_sent[i]} sat\n"
                # result += "Destinations :\n"

                # for addr, value in destinations[i]:
                #     result += f"  → {addr} : {value} sats\n"
                # result += "\n"

            return result


        except Exception as e:
            logger.error(f"Failed to process: {e}", extra={"address": address}, exc_info=True)
            return None


# Singleton instance for the analyzer
_transactions_analyser_instance = None

def get_transactions_analyser_client() -> TransactionAnalyzer:
    """Get or create the Transactions Analyzer client singleton instance."""
    global _transactions_analyser_instance
    if _transactions_analyser_instance is None:
        _transactions_analyser_instance = TransactionAnalyzer()
    return _transactions_analyser_instance