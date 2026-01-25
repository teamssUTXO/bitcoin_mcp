import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from src.core.network import get_network_analyser_client


logger = logging.getLogger(__name__)

def get_bitcoin_network_overview() -> Optional[str]:
    """
    Use this for general Bitcoin blockchain questions about current state, health, or status.

    Provides comprehensive network overview across five key areas:

    **Network Statistics:**
    - Current market price in USD
    - Network hashrate in TH/s (total mining power)
    - Current mining difficulty
    - Next difficulty adjustment block height

    **Block Metrics:**
    - Blocks mined in the last 24 hours
    - Total blocks in the blockchain
    - Average time between blocks (target: 10 minutes)
    - Average block size in bytes

    **Transaction Activity:**
    - Total transactions in the last 24 hours
    - Estimated BTC sent in 24h
    - Estimated transaction volume in USD

    **Mining Economics:**
    - BTC mined in the last 24 hours (new supply)
    - Total transaction fees collected in 24h (in BTC)
    - Total miner revenue in BTC and USD

    **Supply Information:**
    - Total BTC in circulation
    """
    try:
        logger.info("Tool Called : get_bitcoin_network_overview")

        network_analyzer = get_network_analyser_client()
        data: str = network_analyzer.get_network_stats()

        logger.info("Tool get_bitcoin_network_overview succeeded")

        return data

    except Exception as e:
        logger.error(f"Unexpected error in tool get_bitcoin_network_overview : {e}", exc_info=True)
        return None

def get_bitcoin_network_recommended_fees() -> Optional[str]:
    """
    Use this to get current recommended Bitcoin transaction fees for different confirmation speed priorities.

    Returns fee recommendations in string format with four priority levels:
    - **Fastest** (~10 minutes): Highest fee for next block inclusion
    - **Half-hour** (~30 minutes): Medium-high fee for confirmation within 30 min
    - **Standard** (~60 minutes): Medium fee for confirmation within 1 hour
    - **Economy**: Lowest fee for non-urgent transactions

    Each recommendation includes:
    - Fee rate in sat/vB (satoshis per virtual byte)
    - Estimated confirmation time
    - Approximate total cost in BTC for a typical transaction

    Fees are dynamic and change based on current network congestion and mempool size.

    Use cases: When you need to know how much to pay for a Bitcoin transaction, to optimize transaction costs vs. speed, or to check if the network is congested.
    """
    try:
        logger.info("Tool Called : get_bitcoin_network_recommended_fees")

        network_analyzer = get_network_analyser_client()
        data: str = network_analyzer.get_network_recommended_fees()

        logger.info("Tool get_bitcoin_network_recommended_fees succeeded")

        return data

    except Exception as e:
        logger.error(f"Unexpected error in tool get_bitcoin_network_recommended_fees : {e}", exc_info=True)
        return None

def get_bitcoin_network_health() -> Optional[str]:
    """
    Use this to get a simplified health assessment of the Bitcoin network with a single score and status label.

    Returns a concise health summary in string format:
    - Network status label (e.g., "Healthy", "Degraded", "Critical")
    - Numerical health score out of 100 (0-100 scale)

    The health score is a composite metric that considers factors like block production consistency, hashrate stability and transactions volume.
    """
    try:
        logger.info("Tool Called : get_bitcoin_network_health")

        network_analyzer = get_network_analyser_client()
        data: str = network_analyzer.get_network_health()

        logger.info("Tool get_bitcoin_network_health succeeded")

        return data

    except Exception as e:
        logger.error(f"Unexpected error in tool get_bitcoin_network_health : {e}", exc_info=True)
        return None

def register_network_tools(mcp: FastMCP):
    """Registers all Bitcoin network tools"""
    logger.info("Registering Network Tools...")

    mcp.add_tool(get_bitcoin_network_overview)
    mcp.add_tool(get_bitcoin_network_recommended_fees)
    mcp.add_tool(get_bitcoin_network_health)

    logger.info("Network Tools Registered")
    
    

    
    
    