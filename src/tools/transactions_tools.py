from mcp.server.fastmcp import FastMCP
from src.core.transactions import get_transactions_analyser_client


def get_bitcoin_transaction_infos(txid: str) -> str:
    """
    Use this to get information about a transaction

    Args:
        txid: Transaction ID
    """

    transactions_analyzer = get_transactions_analyser_client()

    data: str = transactions_analyzer.get_tx_info(txid)
    return data


def get_transaction_input_output(txid: str) -> str:
    """
    Use this to get details input and output of a transaction

    Args:
        txid: Transaction ID
    """

    transactions_analyzer = get_transactions_analyser_client()

    data: str = transactions_analyzer.get_tx_inputs_outputs(txid)
    return data


def get_transactions_of_address(address: str) -> str:
    """
    Use this to get address's transactions

    Args:
        address: Address to get transactions
    """

    transactions_analyzer = get_transactions_analyser_client()

    data: str = transactions_analyzer.get_address_transactions(address)
    return data


def register_transactions_tools(mcp: FastMCP):
    """Enregistre tous les tools de transactions Bitcoin"""
    mcp.add_tool(get_bitcoin_transaction_infos)
    mcp.add_tool(get_transaction_input_output)
    mcp.add_tool(get_transactions_of_address)





