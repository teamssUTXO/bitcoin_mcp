from typing import Optional

from mcp.server.fastmcp import FastMCP
from src.core.network import get_network_analyser_client

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

    network_analyzer = get_network_analyser_client()

    data: str = network_analyzer.get_network_stats()
    return data


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

    network_analyzer = get_network_analyser_client()

    data: str = network_analyzer.get_network_recommended_fees()
    return data

def get_bitcoin_network_health() -> Optional[str]:
    """
    Parfait ! Voici la définition optimisée pour get_bitcoin_network_health :

    Outil MCP : get_bitcoin_network_health
    description
    Use this to get a simplified health assessment of the Bitcoin network with a single score and status label.

    Returns a concise health summary in string format:
    - Network status label (e.g., "Healthy", "Degraded", "Critical")
    - Numerical health score out of 100 (0-100 scale)

    The health score is a composite metric that considers factors like block production consistency, hashrate stability and transactions volume.
    """

    network_analyzer = get_network_analyser_client()

    data: str = network_analyzer.get_network_health()
    return data


def register_network_tools(mcp: FastMCP):
    """Registers all Bitcoin network tools"""
    mcp.add_tool(get_bitcoin_network_overview)
    mcp.add_tool(get_bitcoin_network_recommended_fees)
    mcp.add_tool(get_bitcoin_network_health)
    
    

    
    
    