# manually add project root to sys.path => entire repo becomes usable
import sys
import os

from starlette.applications import Starlette
from starlette.routing import Route, Mount

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)

import logging
import argparse
import uvicorn
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from mcp.server.fastmcp import FastMCP, Context

from src.tools.network_tools import register_network_tools
from src.tools.transactions_tools import register_transactions_tools
from src.tools.addresses_tools import register_addresses_tools
from src.tools.market_tools import register_market_tools
from src.tools.mining_tools import register_mining_tools
from src.tools.blocks_tools import register_blocks_tools

from src.log import get_logger


get_logger = get_logger()
logger = logging.getLogger(__name__)
logger.info("Server starting...")

mcp = FastMCP("bitcoin_mcp_server")
logger.info("FastMCP instance initialized")

logger.info("Initializing Tools...")
register_network_tools(mcp)
register_transactions_tools(mcp)
register_addresses_tools(mcp)
register_market_tools(mcp)
register_mining_tools(mcp)
register_blocks_tools(mcp)
logger.info("Tools Initialized")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MCP Server")
    parser.add_argument("--port", "-p", type=int, help="Localhost port to listen on")
    args = parser.parse_args()

    if args.port:
        logger.info(f"Server ready, starting HTTP MCP Server on port {args.port}...")
        app = mcp.sse_app()

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # En production, spécifie les origines autorisées
            allow_credentials=True,
            allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, OPTIONS, etc.)
            allow_headers=["*"],
        )

        uvicorn.run(app, host="0.0.0.0", port=args.port)
    else:
        logger.info("Server ready, starting STDIO MCP Server")
        mcp.run()