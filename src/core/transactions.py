import logging
from typing import Optional, Any
from datetime import datetime

from src.api.mempool_client import get_mempool_client
from src.api.blockchain_client import get_blockchain_client

from src.data.transactions_dataclasses import DataTransactionInfo, DataTxInOut, DataTxOutput, DataTxInput
from src.data.transactions_dataclasses import DataTransactionsAddress

from src.config import Config
from returns.result import Result, Success, Failure
from src.errors import Error, DataValidationError


logger = logging.getLogger(__name__)

class TransactionAnalyzer:
    """Bitcoin Transactions Analyzer"""

    def __init__(self):
        """
        Initialize Bitcoin Transactions Analyzer.
        """
        self.mempool = get_mempool_client()
        self.blockchain = get_blockchain_client()

    async def get_tx_info(self, txid: str) -> Result[str, Error]:
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
        data_result = await self.mempool.get_tx_info(txid)
        if isinstance(data_result, Failure):
            return Failure(data_result.failure())

        data: Any = data_result.unwrap()
        if not data:
            return Failure(DataValidationError(details="Empty response"))

        try:
            infos: DataTransactionInfo = DataTransactionInfo.from_data(data)
        except Exception as e:
            return Failure(DataValidationError(details=str(e)))

            nb_inputs: int = len(infos.vin)
            nb_outputs: int = len(infos.vout)

            fee_btc: float = infos.fee / Config.SATOSHI

            transaction_status: str = "CONFIRMED" if infos.status.get("confirmed") else "UNCONFIRMED"
            transaction_block_time: int = infos.status.get('block_time', 0)
            transaction_block_hash: str = infos.status.get('block_hash', '')
            transaction_block_height: int = infos.status.get('block_height', 0)

            date_str: str = datetime.fromtimestamp(transaction_block_time).strftime(
                '%Y-%m-%d %H:%M:%S') if transaction_block_time else 'UNCONFIRMED'

            total_sats_out: int = sum(out.get('value', 0) for out in infos.vout)
            total_btc_out: float = total_sats_out / Config.SATOSHI

            sat_per_byte: float = infos.fee / infos.size if infos.size > 0 else 0

            status_icon: str = "[CONFIRMED]" if infos.status.get("confirmed") else "[PENDING]"

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

            return Success(result)


    async def get_tx_inputs_outputs(self, txid: str) -> Result[str, Error]:
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
        data_result = await self.mempool.get_tx_info(txid)
        if isinstance(data_result, Failure):
            return Failure(data_result.failure())

        data: Any = data_result.unwrap()
        if not data:
            return Failure(DataValidationError(details="Empty response"))

        try:
            infos: DataTxInOut = DataTxInOut.from_data(data)
        except Exception as e:
            return Failure(DataValidationError(details=str(e)))

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
                detailed_in_lines.append(f"  [IN]  {val:12.8f} BTC | SINCE: {addr}")

            detailed_out_lines: list = []
            for o in outputs:
                addr: str = o.address if o.address else "DATA (OP_RETURN)"
                val: float = o.value / Config.SATOSHI
                detailed_out_lines.append(f"  [OUT] {val:12.8f} BTC | To:   {addr}")

            clean_in_addrs: list = [a for a in addresses_in if a]
            clean_out_addrs: list = [a for a in addresses_out if a]

            list_in_txt: str = "\n".join([f"  - {a}" for a in clean_in_addrs]) if clean_in_addrs else "  - No public address"
            list_out_txt: str = "\n".join([f"  - {a}" for a in clean_out_addrs]) if clean_out_addrs else "  - No standard address"

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

            return Success(result)


    async def get_address_transactions(self, address: str) -> Result[str, Error]:
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
        data_result = await self.blockchain.get_address_info(address)
        if isinstance(data_result, Failure):
            return Failure(data_result.failure())

        data: Any = data_result.unwrap()
        if not data:
            return Failure(DataValidationError(details="Empty response"))

        try:
            infos: DataTransactionsAddress = DataTransactionsAddress.from_data(data)
        except Exception as e:
            return Failure(DataValidationError(details=str(e)))

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

            # Destinations(address + amount)
            # Removed because too many tokens
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

            return Success(result)


# Singleton instance for the analyzer
_transactions_analyser_instance = None

def get_transactions_analyser_client() -> TransactionAnalyzer:
    """Get or create the Transactions Analyzer client singleton instance."""
    global _transactions_analyser_instance
    if _transactions_analyser_instance is None:
        _transactions_analyser_instance = TransactionAnalyzer()
    return _transactions_analyser_instance
