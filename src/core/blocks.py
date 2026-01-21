from typing import Optional
from datetime import datetime, timedelta

from src.api.blockchain_client import get_blockchain_client
from src.api.mempool_client import get_mempool_client

from src.data.block_dataclasses import DataLatestBlock, DataLatestBlocks

class BlockAnalyzer:
    """Analyseur de blocs Bitcoin"""

    def __init__(self):
        """
        Initialise l'analyseur de blocs.
        """
        self.mempool = get_mempool_client()
        self.blockchain = get_blockchain_client()

    def get_latest_block_summary(self) -> Optional[str]:
        """
        Récupère un résumé du dernier bloc miné.

        Returns:
            str: Résumé du dernier bloc ou None en cas d'erreur
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
                f"=== Dernier Bloc Miné ===\n"
                f"Hauteur: #{infos.height:,}\n"
                f"Hash: {infos.hash}\n"
                f"Horodatage: {date_str} (il y a {time_ago_str})\n"
                f"Index du block: {infos.block_index:,}\n"
            )
            return result

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_block_by_height(self, height: int) -> Optional[str]:
        """
        Récupère le hash d'un bloc avec une hauteur donnée.

        Args:
            height: Hauteur du bloc recherché

        Returns:
            str: Hash du bloc ou None en cas d'erreur
        """
        try:
            block_hash: str = str(self.mempool.get_block_height(height))
            if not block_hash:
                return None

            return f"Hash du bloc #{height:,}: {block_hash}"

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_latest_blocks_info(self) -> Optional[str]:
        """
        Récupère les informations sur les 10 derniers blocs.

        Returns:
            str: Infos des derniers blocs formatées ou None en cas d'erreur
        """
        try:
            data: list = self.mempool.get_blocks_info()
            if not data:
                return None

            infos: DataLatestBlocks = DataLatestBlocks.from_data(data)

            result: list = ["=== 10 Derniers Blocs ==="]

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
                    f"=== Informations (10 derniers blocs) ===\n"
                    f"\nBloc #{infos.heights[i]:,} | ID: {infos.ids[i]}\n"
                    f"Date: {infos.timestamps[i]}\n"
                    f"Transactions: {infos.txs_count[i]:,}\n"
                    f"Taille: {infos.sizes[i]:.2f} MB\n"
                    f"Weight: {infos.weights[i]:,}\n"
                    f"Frais totaux: {infos.totalsFees[i]:,} sats / Frais moyens: {infos.avgsFeeRate[i]} sat/vB\n"
                    f"Récompense: {infos.rewards[i]:,} sats\n"
                    f"Pool: {infos.pools_slug[i]}\n"
                    f"Nonce: {infos.nonces[i]}"
                    f"=== Statistiques (10 derniers blocs) ===\n"
                    f"Total transactions: {total_tx:,}\n"
                    f"Moyenne par bloc: {avg_tx:.0f} tx\n"
                    f"Taille moyenne: {avg_size / 1_000_000:.2f} MB\n"
                    f"Temps moyen entre blocs: {avg_time:.2f} min"
                )

            return "\n".join(result)

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


# Singleton instance for the analyzer
_blocks_analyser_instance = None

def get_blocks_analyser_client() -> BlockAnalyzer:
    """Get or create the Blocks Analyzer client singleton instance."""
    global _blocks_analyser_instance
    if _blocks_analyser_instance is None:
        _blocks_analyser_instance = BlockAnalyzer()
    return _blocks_analyser_instance