from typing import Optional

from mcp.server.fastmcp import FastMCP
from src.core.mining import get_mining_analyser_client


def get_top_10_mining_pools_rank() -> Optional[str]:
    """
    Use this to get top 10 mining pools rank
    """

    mining_analyzer = get_mining_analyser_client()

    data: str = mining_analyzer.get_mining_pools_ranking()
    return data


def get_mining_pools_hashrates_3month() -> Optional[str]:
    """
    Use this to get top 10 mining pools hashrates 3month
    """

    mining_analyzer = get_mining_analyser_client()

    data: str = mining_analyzer.get_mining_pool_hashrates()
    return data


def get_top1_mining_pool() -> Optional[str]:
    """
    Use this to get the top 1 pool actually
    """

    mining_analyzer = get_mining_analyser_client()

    data: str = mining_analyzer.get_top_pool()
    return data

def get_mining_pool_by_slug(slug: str) -> Optional[str]:
    """
    Use this to get information about a mining pool by slug

    Args:
        slug: slug of the mining pool
    """

    mining_analyzer = get_mining_analyser_client()

    data: str = mining_analyzer.get_pool_by_slug(slug)
    return data

def get_bitcoin_network_mining_pools_statistics() -> str:
    """
    Use this to get statistics about bitcoin mining pools
    """

    mining_analyzer = get_mining_analyser_client()

    data: str = mining_analyzer.get_mining_statistics()
    return data


def register_mining_tools(mcp: FastMCP):
    """Enregistre tous les tools de mining pools du réseau Bitcoin"""
    mcp.add_tool(get_mining_pools_hashrates_3month)
    mcp.add_tool(get_top_10_mining_pools_rank)
    mcp.add_tool(get_bitcoin_network_mining_pools_statistics)
    mcp.add_tool(get_top1_mining_pool)
    mcp.add_tool(get_mining_pool_by_slug)





