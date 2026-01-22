from typing import Optional

from mcp.server.fastmcp import FastMCP
from src.core.transactions import get_transactions_analyser_client


def get_bitcoin_transaction_infos(txid: str) -> Optional[str]:
    """
    Use this to get comprehensive information about a specific Bitcoin transaction using its transaction ID (txid).

    Returns detailed metrics in string format across four categories:

    **Transaction Status:**
    - Current status (Confirmed/Unconfirmed with visual indicator)
    - Transaction date and time

    **Economics & Flow:**
    - Total amount transferred in BTC
    - Transaction fees paid in BTC
    - Fee rate in sat/vB (satoshis per virtual byte)

    **Technical Structure:**
    - Transaction size in bytes
    - Number of inputs (sources of funds)
    - Number of outputs (destinations)

    **Block Information (if confirmed):**
    - Block height where transaction was included
    - Block hash containing the transaction

    The txid is a unique 64-character hexadecimal identifier for each Bitcoin transaction.

    Use cases: When you need to verify a payment, check transaction status, analyze fees paid, or investigate transaction details.
    """

    if not txid:
        return "no parameters"

    transactions_analyzer = get_transactions_analyser_client()

    data: str = transactions_analyzer.get_tx_info(txid)
    return data


def get_transaction_input_output(txid: str) -> Optional[str]:
    """
    Use this to get detailed input and output breakdown of a Bitcoin transaction, including all addresses and amounts involved.

    Returns comprehensive flow analysis in string format across four sections:

    **Accounting Summary:**
    - Total incoming volume (sum of all inputs) in BTC
    - Total outgoing volume (sum of all outputs) in BTC
    - Network fees paid (difference between inputs and outputs) in BTC

    **Detailed UTXO Flow:**
    - List of all incoming movements (inputs) with:
      - Source address
      - Amount in BTC
      - Previous transaction reference (prev_out)
    - List of all outgoing movements (outputs) with:
      - Destination address
      - Amount in BTC
      - Output index

    **Participant Registry:**
    - Complete list of sender addresses (count included)
    - Complete list of recipient addresses (count included)

    This provides full transparency into the transaction's inputs (where funds came from) and outputs (where funds went), essential for tracking fund flow and identifying all parties involved.

    Use cases: When you need to trace Bitcoin flow, identify sender/recipient addresses, analyze UTXO structure, or investigate complex multi-party transactions.
    """

    if not txid:
        return "no parameters"

    transactions_analyzer = get_transactions_analyser_client()

    data: str = transactions_analyzer.get_tx_inputs_outputs(txid)
    return data


def get_transactions_of_address(address: str) -> Optional[str]:
    """
    Use this to get the complete transaction history of a Bitcoin address.

    Returns a chronological list of all transactions in string format, with each transaction showing:
    - Transaction ID (txid) - unique identifier for the transaction
    - Transaction date and time
    - Amount sent in satoshis

    This provides the full transaction history for an address, allowing you to see all incoming and outgoing payments over time. Each transaction can be further investigated using `get_bitcoin_transaction_infos` or `get_transaction_input_output` with the returned txid.

    Accepts any Bitcoin address format (Legacy, SegWit, Bech32).

    Use cases: When you need to audit an address's activity, track payment history, verify specific transactions, or investigate suspicious activity.
    """

    if not address:
        return "no parameters"

    transactions_analyzer = get_transactions_analyser_client()

    data: str = transactions_analyzer.get_address_transactions(address)
    return data


def register_transactions_tools(mcp: FastMCP):
    """Registers all Bitcoin transactions tools"""
    mcp.add_tool(get_bitcoin_transaction_infos)
    mcp.add_tool(get_transaction_input_output)
    mcp.add_tool(get_transactions_of_address)





