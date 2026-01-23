from typing import Optional

from mcp.server.fastmcp import FastMCP

from src.core.addresses import get_addresses_analyser_client


def get_info_about_address(address: str) -> Optional[str]:
    """
    Use this to get comprehensive information about a Bitcoin address including balance, transaction activity, and spending patterns.

    Returns detailed metrics in string format:
    - Current confirmed and unconfirmed balance (in BTC and satoshis)
    - Address category and status
    - Total transaction count (confirmed + mempool)
    - Received outputs count and total amount
    - Spent outputs count and total amount

    Accepts any Bitcoin address format (Legacy, SegWit, Bech32).

    Use cases: When you need a complete snapshot of an address's financial activity and current state.
    """

    if not address:
        return "no parameters"

    addresses_analyzer = get_addresses_analyser_client()

    data: str = addresses_analyzer.get_address_info(address)
    return data


def get_address_overview(address: str) -> Optional[str]:
    """
    Use this to get a simplified overview of a Bitcoin address focusing on balance and cumulative transaction totals.

    Returns detailed metrics in string format:
    - Current balance (in BTC)
    - Total amount ever received (in BTC)
    - Total amount ever sent (in BTC)
    - Total number of transactions

    Accepted Bitcoin address format : base58 or hash160.

    Use cases: When you need a quick financial summary without granular details.
    """

    if not address:
        return "no parameters"

    addresses_analyzer = get_addresses_analyser_client()

    data: str = addresses_analyzer.get_address_info_overview(address)
    return data


def register_addresses_tools(mcp: FastMCP):
    """Registers all Bitcoin address tools"""
    mcp.add_tool(get_info_about_address)
    mcp.add_tool(get_address_overview)





