import logging
from typing import Optional
from datetime import datetime, timedelta

from src.api.blockchain_client import get_blockchain_client
from src.api.mempool_client import get_mempool_client

from src.data.block_dataclasses import DataLatestBlock, DataLatestBlocks

logger = logging.getLogger(__name__)


class BlockAnalyzer:
    """Bitcoin Blocks Analyzer"""

    def __init__(self):
        """
        Initialize Blocks Analyzer.
        """
        self.mempool = get_mempool_client()
        self.blockchain = get_blockchain_client()

    def get_latest_block_summary(self) -> Optional[str]:
        """
        Retrieves a summary of the most recently mined block.

        Returns:
            A Markdown formatted string including:
            - Block height and unique hash.
            - Detailed timestamp (UTC and relative time).
            - Internal block index.
            Returns None if an API error occurs or data is missing.
        """
        try:
            data: dict = self.blockchain.get_latest_block()
            if not data:
                return None

            infos: DataLatestBlock = DataLatestBlock.from_data(data)

            date_str: str = datetime.fromtimestamp(infos.timestamp).strftime('%Y-%m-%d %H:%M:%S') if infos.timestamp else 'N/A'
            time_ago: timedelta = datetime.now() - datetime.fromtimestamp(infos.timestamp) if infos.timestamp else None
            time_ago_str: str = f"{int(time_ago.total_seconds() / 60)} minutes" if time_ago else "N/A"

            result: str = (
                f"## Latest Mined Block\n"
                f"Height: {infos.height}\n"
                f"Hash: {infos.hash}\n"
                f"Timestamp: {date_str} ({time_ago_str} ago)\n"
                f"Block Index: {infos.block_index}"
            )
            return result


        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None

    def get_block_by_height(self, height: int) -> Optional[str]:
        """
        Retrieves the block hash for a specific block height.

        Args:
            height: The height of the block to search for.

        Returns:
            A formatted string containing the block height and its corresponding hash.
            Returns None if the block is not found or an API error occurs.
        """
        try:
            block_hash: str = self.mempool.get_block_height(height)
            if not block_hash:
                return None

            return f"Hash du bloc #{height:,}: {block_hash}"


        except Exception as e:
            logger.error(f"Failed to process: {e}", extra={"height": height}, exc_info=True)
            return None

    def get_latest_blocks_info(self) -> Optional[str]:
        """
        Retrieves detailed information and statistics for the last 10 mined blocks.

        Returns:
            A Markdown formatted string including:
            - Individual block details (Height, ID, Timestamp, TX count).
            - Technical data per block (Size, Weight, Fees, Reward, Pool name).
            - Aggregate statistics (Total/average transactions, average size, and average block time).
            Returns None if an API error occurs or data is empty.
        """
        try:
            data: list = self.mempool.get_blocks_info()
            if not data:
                return None

            infos: DataLatestBlocks = DataLatestBlocks.from_data(data)

            result: list = ["## Last 10 Blocks Details"]

            total_tx: int = sum(infos.txs_count)
            avg_tx: float = total_tx / len(data)
            total_size: int = sum(infos.sizes)
            avg_size: float = total_size / len(data)

            if len(infos.timestamps) >= 2:
                time_diffs: list = [infos.timestamps[i] - infos.timestamps[i + 1] for i in
                                    range(len(infos.timestamps) - 1)]
                avg_time: float = sum(time_diffs) / len(time_diffs) / 60  # en minutes
            else:
                avg_time: int = 0

            for i in range(len(data)):
                result.append(
                    f"#### Block {infos.heights[i]} | {infos.ids[i]}\n"
                    f"Time: {infos.timestamps[i]}\n"
                    f"Transactions: {infos.txs_count[i]}\n"
                    f"Size: {infos.sizes[i]:.2f} MB | Weight: {infos.weights[i]}\n"
                    f"Fees: {infos.totalsFees[i]} sat total | {infos.avgsFeeRate[i]} sat/vB avg\n"
                    f"Reward: {infos.rewards[i]} sat\n"
                    f"Pool: {infos.pools_slug[i]}\n"
                    f"Nonce: {infos.nonces[i]}\n\n"
                    f"## Aggregate Statistics\n"
                    f"Total Transactions: {total_tx}\n"
                    f"Average per Block: {avg_tx:.0f}\n"
                    f"Average Size: {avg_size / 1_000_000:.2f} MB\n"
                    f"Average Block Time: {avg_time:.2f} min"
                )

            return "\n".join(result)


        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None


# Singleton instance for the analyzer
_blocks_analyser_instance = None

def get_blocks_analyser_client() -> BlockAnalyzer:
    """Get or create the Blocks Analyzer client singleton instance."""
    global _blocks_analyser_instance
    if _blocks_analyser_instance is None:
        _blocks_analyser_instance = BlockAnalyzer()
    return _blocks_analyser_instance