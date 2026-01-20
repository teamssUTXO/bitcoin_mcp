from typing import Optional

from mcp.server.fastmcp import FastMCP
from src.core.blocks import get_blocks_analyser_client


def get_summary_of_latest_block() -> Optional[str]:
    """
    Use this to get a summary of the latest block mined
    """

    blocks_analyzer = get_blocks_analyser_client()

    data: str = blocks_analyzer.get_latest_block_summary()
    return data


def get_block_hash_with_height(height: int) -> Optional[str]:
    """
    Use this to get a block's hash with his height

    Args:
        height: block height (int)
    """

    blocks_analyzer = get_blocks_analyser_client()

    data: str = blocks_analyzer.get_block_by_height(height)
    return data


def get_10_latest_blocks_informations() -> Optional[str]:
    """
    Use this to get information and statistics about 10 latest blocks mined
    """

    blocks_analyzer = get_blocks_analyser_client()

    data: str = blocks_analyzer.get_latest_blocks_info()
    return data


def register_blocks_tools(mcp: FastMCP):
    """Enregistre tous les tools de blocs du réseau Bitcoin"""
    mcp.add_tool(get_10_latest_blocks_informations)
    mcp.add_tool(get_block_hash_with_height)
    mcp.add_tool(get_summary_of_latest_block)





