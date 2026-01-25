import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from src.core.addresses import get_addresses_analyser_client


logger = logging.getLogger(__name__)

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
    try:
        logger.info("Tool called : get_info_about_address")

        addresses_analyzer = get_addresses_analyser_client()
        data: str = addresses_analyzer.get_address_info(address)

        logger.info("Tool get_info_about_address succeeded")

        return data


    except TypeError as e:
        logger.error(f"Invalid call or missing parameter: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in tool get_info_about_address : {e}", exc_info=True)
        return None


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
    try:
        logger.info("Tool called : get_address_overview")

        addresses_analyzer = get_addresses_analyser_client()
        data: str = addresses_analyzer.get_address_info_overview(address)

        logger.info("Tool get_address_overview succeeded")

        return data


    except TypeError as e:
        logger.error(f"Invalid call or missing parameter: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in tool get_address_overview : {e}", exc_info=True)
        return None


def register_addresses_tools(mcp: FastMCP):
    """Registers all Bitcoin address tools"""
    logger.info("Registering Addresses Tools...")

    mcp.add_tool(get_info_about_address)
    mcp.add_tool(get_address_overview)

    logger.info("Addresses Tools Registered")





