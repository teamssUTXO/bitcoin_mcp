from mcp.server.fastmcp import FastMCP
from src.core.network import get_network_analyser_client

def get_bitcoin_network_overview() -> str:
    """
    Use this for general Bitcoin blockchain questions about current state, health, or status.

    Provides comprehensive network overview:
    - Current block height and latest block info
    - Network hashrate and mining difficulty
    - Average block time (10min target vs actual)
    - Total circulating supply and remaining to mine
    - Network uptime and consensus status
    
    Use cases: "How is Bitcoin doing?", "What's the network status?", "Is Bitcoin working normally?"
    """

    network_analyzer = get_network_analyser_client()

    data: str = network_analyzer.get_network_stats()
    return data


def get_bitcoin_network_recommended_fees() -> str:
    """
    Use this to get bitcoin transactions recommended fees
    """

    network_analyzer = get_network_analyser_client()

    data: str = network_analyzer.get_network_recommended_fees()
    return data

def get_bitcoin_network_health() -> str:
    """
    Use this to get the global bitcoin network health
    """

    network_analyzer = get_network_analyser_client()

    data: str = network_analyzer.get_network_health()
    return data


def register_network_tools(mcp: FastMCP):
    """Enregistre tous les tools réseau"""
    mcp.add_tool(get_bitcoin_network_overview)
    mcp.add_tool(get_bitcoin_network_recommended_fees)
    mcp.add_tool(get_bitcoin_network_health)
    
    

    
    
    