# manually add project root to sys.path => entire repo becomes usable
import sys
import os
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)


from mcp.server.fastmcp import FastMCP

from src.tools.network_tools import register_network_tools
# from src.tools.transaction_tools import register_transaction_tools
# from src.tools.address_tools import register_address_tools
# from src.tools.market_tools import register_market_tools
# from src.tools.mining_tools import register_mining_tools

mcp = FastMCP("bitcoin_mcp_server")


register_network_tools(mcp)
# register_transaction_tools(mcp)
# register_address_tools(mcp)
# register_market_tools(mcp)
# register_mining_tools(mcp)

if __name__ == "__main__":
    mcp.run()