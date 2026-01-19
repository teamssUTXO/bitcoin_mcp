from mcp.server.fastmcp import FastMCP
from src.core.network import NetworkAnalyzer
# from ..utils.formatting import format_network_report

def get_bitcoin_network_overview() -> dict:
    """
    USE THIS FIRST for general Bitcoin blockchain questions about current state, health, or status.

    Provides comprehensive network overview:
    - Current block height and latest block info
    - Network hashrate and mining difficulty
    - Average block time (10min target vs actual)
    - Total circulating supply and remaining to mine
    - Network uptime and consensus status
    
    Use cases: "How is Bitcoin doing?", "What's the network status?", "Is Bitcoin working normally?"
    """

    network_analyzer = NetworkAnalyzer()

    status: dict = network_analyzer.get_network_overview()
    return status



def register_network_tools(mcp: FastMCP):
    """Enregistre tous les tools réseau"""
    mcp.add_tool(get_bitcoin_network_overview)
    
    

    
    
    