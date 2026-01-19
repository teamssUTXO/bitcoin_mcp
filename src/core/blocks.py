from typing import Optional
from datetime import datetime

from api.blockchain_client import get_blockchain_client
from src.api.mempool_client import get_mempool_client

from src.data.block_dataclasses import LatestBlock, LatestsBlocks

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
            block = self.blockchain.get_latest_block()
            if not block:
                return None

            infos = LatestBlock.from_data(block)


            date_str = datetime.fromtimestamp(infos.timestamp).strftime('%Y-%m-%d %H:%M:%S') if infos.timestamp else 'N/A'

            # Calcul du temps écoulé
            time_ago = datetime.now() - datetime.fromtimestamp(infos.timestamp) if infos.timestamp else None
            time_ago_str = f"{int(time_ago.total_seconds() / 60)} minutes" if time_ago else "N/A"

            result = (
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
            block_hash = self.mempool.get_block_height(height)
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
            blocks = self.mempool.get_blocks_info()
            if not blocks:
                return None

            infos = LatestsBlocks.from_data(blocks)

            result_lines = ["=== 10 Derniers Blocs ==="]

            for i in range(len(blocks)):
                result_lines.append(
                    f"\nBloc #{infos.heights[i]:,} | ID: {infos.ids[i]}\n"
                    f"Date: {infos.timestamps[i]}\n"
                    f"Transactions: {infos.txs_count[i]:,}\n"
                    f"Taille: {infos.sizes[i]:.2f} MB\n"
                    f"Weight: {infos.weights[i]:,}\n"
                    f"Frais totaux: {infos.totalsFees[i]:,} sats / Frais moyens: {infos.avgsFeeRate[i]} sat/vB\n"
                    f"Récompense: {infos.rewards[i]:,} sats\n"
                    f"Pool: {infos.pools_slug[i]}\n"
                    f"Nonce: {infos.nonces[i]}"

                    
                )

            return "\n".join(result_lines)

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_block_stats(self) -> Optional[str]:
        """
        Calcule des statistiques sur les 10 derniers blocs.

        Returns:
            str: Statistiques des blocs ou None en cas d'erreur
        """
        try:
            blocks = self.mempool.get_blocks_info()
            if not blocks:
                return None

            infos = LatestsBlocks.from_data(blocks)

            total_tx = sum(infos.txs_count)
            avg_tx = total_tx / len(blocks)
            total_size = sum(infos.sizes)
            avg_size = total_size / len(blocks)

            # Calcul du temps moyen entre blocs
            if len(infos.timestamps) >= 2:
                time_diffs = [infos.timestamps[i] - infos.timestamps[i + 1] for i in range(len(infos.timestamps) - 1)]
                avg_time = sum(time_diffs) / len(time_diffs) / 60  # en minutes
            else:
                avg_time = 0

            result = (
                f"=== Statistiques (10 derniers blocs) ===\n"
                f"Total transactions: {total_tx:,}\n"
                f"Moyenne par bloc: {avg_tx:.0f} tx\n"
                f"Taille moyenne: {avg_size / 1_000_000:.2f} MB\n"
                f"Temps moyen entre blocs: {avg_time:.2f} min"
            )
            return result

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None
