import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from src.core.mining import get_mining_analyser_client


logger = logging.getLogger(__name__)

def get_top_10_mining_pools_rank() -> Optional[str]:
    """
    Use this to get the ranking of the top 10 Bitcoin mining pools based on the number of blocks mined.

    Returns detailed metrics in string format for each of the 10 leading mining pools:
    - Pool name and rank position (1-10)
    - Total number of blocks mined by the pool
    - Percentage of total blocks mined (pool's share of network hashrate)
    - Grand total of blocks across all pools

    This ranking represents the current distribution of Bitcoin mining power and shows which pools control the most hashrate.

    Use cases: When you need to understand mining centralization, identify the dominant mining pools, or analyze the distribution of network hashrate.
    """
    try:
        logger.info("Tool Called : get_top_10_mining_pools_ranking")

        mining_analyzer = get_mining_analyser_client()
        data: str = mining_analyzer.get_mining_pools_ranking()

        logger.info("Tool get_top_10_mining_pools_ranking succeeded")

        return data

    except Exception as e:
        logger.error(f"Unexpected error in tool get_top_10_mining_pools_rank : {e}", exc_info=True)
        return None


def get_mining_pools_hashrates_3month() -> Optional[str]:
    """
    Use this to get the top 10 Bitcoin mining pools ranked by their average hashrate over the last 3 months.

    Returns detailed metrics in string format for each of the 10 leading mining pools:
    - Pool rank position (1-10)
    - Pool name
    - Average hashrate in EH/s (Exahashes per second) over the 3-month period
    - Network share percentage (portion of total Bitcoin network hashrate)

    This data shows the historical performance and consistency of mining pools over a 3-month timeframe, providing a more stable view than current block count alone.

    Use cases: When you need to analyze mining pool trends over time, understand hashrate distribution patterns, or identify consistently dominant pools.
    """
    try:
        logger.info("Tool Called : get_top_10_mining_pools_hashrates_3month")
        mining_analyzer = get_mining_analyser_client()
        data: str = mining_analyzer.get_mining_pool_hashrates()

        logger.info("Tool get_top_10_mining_pools_hashrates_3month succeeded")

        return data

    except Exception as e:
        logger.error(f"Unexpected error in tool get_top_10_mining_pools_hashrates_3month : {e}", exc_info=True)
        return None


def get_top1_mining_pool() -> Optional[str]:
    """
    Use this to get information about the current #1 ranked Bitcoin mining pool based on blocks mined over the last 3 months.

    Returns detailed metrics in string format for the leading mining pool only:
    - Pool name
    - Pool slug identifier (used for searching specific pool details)
    - Total number of blocks mined in the last 3 months
    - Dominance percentage (share of all blocks mined in the 3-month period)
    - Link to pool information page

    This provides quick access to the most dominant mining pool without needing to retrieve data for all top pools.

    Use cases: When you only need to know who currently dominates Bitcoin mining, to check if mining centralization is concerning, or to quickly identify the market leader.
    """
    try:
        logger.info("Tool Called : get_top1_mining_pool")

        mining_analyzer = get_mining_analyser_client()
        data: str = mining_analyzer.get_top_pool()

        logger.info("Tool get_top1_mining_pool succeeded")

        return data

    except Exception as e:
        logger.error(f"Unexpected error in tool get_top1_mining_pool : {e}", exc_info=True)
        return None

def get_mining_pool_by_slug(slug: str) -> Optional[str]:
    """
    Use this to get comprehensive information about a specific Bitcoin mining pool using its unique slug identifier.

    Returns detailed metrics in string format for the requested mining pool:
    - Pool name
    - Official website link
    - Current hashrate (mining power)
    - Number of blocks found/mined
    - Network share percentage (portion of total Bitcoin blocks)
    - Pool's Bitcoin addresses used for receiving block rewards

    The slug is a unique identifier for each mining pool (e.g., "foundry-usa", "antpool", "f2pool"). You can obtain slugs from `get_top1_mining_pool` or `get_top_10_mining_pools_rank`.

    Use cases: When you need detailed information about a specific mining pool that you already know by name or slug, to investigate a pool's addresses, or to verify a pool's technical specifications.
    """
    try:
        logger.info("Tool Called : get_mining_pool_by_slug")

        mining_analyzer = get_mining_analyser_client()
        data: str = mining_analyzer.get_pool_by_slug(slug)

        logger.info("Tool get_mining_pool_by_slug succeeded")

        return data

    except TypeError as e:
        logger.error(f"Invalid call or missing parameter: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in tool get_mining_pool_by_slug : {e}", exc_info=True)
        return None

def get_bitcoin_network_mining_pools_statistics() -> Optional[str]:
    """
    Use this to get aggregate statistics and analysis of the Bitcoin mining pool ecosystem.

    Returns comprehensive metrics in string format about the entire mining landscape:

    **Global Statistics:**
    - Total number of active mining pools tracked
    - Total blocks mined across all pools
    - Average blocks mined per pool

    **Network Dominance Analysis:**
    - Name of the current leading pool
    - Number of blocks mined by the leader
    - Leader's dominance percentage (share of total network)

    **Power Distribution Insights:**
    - Smallest pool's block count (weakest actor)
    - Ratio of leader's performance compared to average (centralization indicator)

    This tool provides a macro view of mining centralization and competition in the Bitcoin network.

    Use cases: When you need to understand the overall mining landscape, assess centralization risk, or compare the gap between dominant and small pools.
    """
    try:
        logger.info("Tool Called : get_bitcoin_network_mining_pools_statistics")

        mining_analyzer = get_mining_analyser_client()
        data: str = mining_analyzer.get_mining_statistics()

        logger.info("Tool get_bitcoin_network_mining_pools_statistics succeeded")

        return data

    except Exception as e:
        logger.error(f"Unexpected error in tool get_info_about_address : {e}", exc_info=True)
        return None

def register_mining_tools(mcp: FastMCP):
    """Registers all Bitcoin mining tools"""
    logger.info("Registering Mining Tools...")

    mcp.add_tool(get_mining_pools_hashrates_3month)
    mcp.add_tool(get_top_10_mining_pools_rank)
    mcp.add_tool(get_bitcoin_network_mining_pools_statistics)
    mcp.add_tool(get_top1_mining_pool)
    mcp.add_tool(get_mining_pool_by_slug)

    logger.info("Mining Tools Registered")





