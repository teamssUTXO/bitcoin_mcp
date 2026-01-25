import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from src.core.blocks import get_blocks_analyser_client

logger = logging.getLogger(__name__)

def get_summary_of_latest_block() -> Optional[str]:
    """
    Use this to get a summary of the most recently mined block on the Bitcoin blockchain.

    Returns detailed metrics in string format:
    - Block height (current blockchain tip)
    - Block hash
    - Timestamp of when the block was mined
    - Block Index

    Use cases: When you need current blockchain state information, to verify the latest block, or to check recent mining activity.
    """
    try:
        logger.info("Tool called : get_summary_of_latest_block")

        blocks_analyzer = get_blocks_analyser_client()
        data: str = blocks_analyzer.get_latest_block_summary()

        logger.info("Tool get_summary_of_latest_block succeeded")

        return data

    except Exception as e:
        logger.error(f"Unexpected error in tool get_summary_of_latest_block : {e}", exc_info=True)
        return None


def get_block_hash_with_height(height: int) -> Optional[str]:
    """
    Use this to retrieve the unique hash identifier of a Bitcoin block by specifying its height (position in the blockchain).

    Returns the block hash in string format for the given height.

    Block height represents the block's position in the blockchain (e.g., height 0 is the Genesis block, height 875000 is the 875,000th block).

    Use cases: When you need to identify a specific block by its position, to verify block integrity, or to look up historical blocks.
    """
    try:
        logger.info("Tool called : get_block_hash_with_height")

        blocks_analyzer = get_blocks_analyser_client()
        data: str = blocks_analyzer.get_block_by_height(height)

        logger.info("Tool get_block_hash_with_height succeeded")
        return data


    except TypeError as e:
        logger.error(f"Invalid call or missing parameter: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in tool get_block_hash_with_height : {e}", exc_info=True)
        return None


def get_10_latest_blocks_informations() -> Optional[str]:
    """
    Use this to get detailed information and statistics about the 10 most recently mined Bitcoin blocks.

    Returns comprehensive metrics in string format for each of the last 10 blocks:
    - Block height and unique identifier (hash)
    - Mining timestamp
    - Transaction count
    - Block size (in MB) and weight
    - Total fees collected and average fee rate (sat/vB)
    - Block reward (in satoshis)
    - Mining pool that found the block
    - Nonce value

    Also includes aggregate statistics across all 10 blocks:
    - Total number of transactions
    - Average transactions per block
    - Average block size
    - Average time between blocks (in minutes)

    Use cases: When you need to analyze recent blockchain activity trends, compare mining pool performance, or monitor network congestion.
    """
    try :
        logger.info("Tool called : get_10_latest_blocks_informations")

        blocks_analyzer = get_blocks_analyser_client()
        data: str = blocks_analyzer.get_latest_blocks_info()

        logger.info("Tool get_10_latest_blocks_informations succeeded")

        return data

    except Exception as e:
        logger.error(f"Unexpected error in tool get_10_latest_blocks_informations : {e}", exc_info=True)
        return None


def register_blocks_tools(mcp: FastMCP):
    """Registers all Bitcoin network tools"""
    logger.info("Registering Blocks Tools...")

    mcp.add_tool(get_10_latest_blocks_informations)
    mcp.add_tool(get_block_hash_with_height)
    mcp.add_tool(get_summary_of_latest_block)

    logger.info("Blocks Tools Registered")





