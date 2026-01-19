from typing import Optional

from src.api.mempool_client import get_mempool_client
from src.data.mining_dataclasses import RankingMiningPools, HashratesMiningPools, TopMiningPool, MiningPoolBySlug


class MiningPoolAnalyzer:
    """Analyseur de mining pools"""

    def __init__(self):
        """
        Initialise l'analyseur de mining pools.
        """
        self.mempool = get_mempool_client() # le client mempool


    def get_mining_pools_ranking(self) -> Optional[str]:
        """
        Récupère le top 10 des mining pools sur 3 mois.

        Returns:
            str: Classement formaté ou None en cas d'erreur
        """
        try:
            pools: dict = self.mempool.get_mining_pools_rank()
            if not pools:
                return None

            infos: RankingMiningPools = RankingMiningPools.from_data(pools)

            result: str = "=== Top Mining Pools (3 mois) ===\n"

            for i, pool in enumerate(infos.pools, 1):
                name: str = pool.get('name', 'Unknown')
                block_count: int = pool.get('blockCount', 0)
                percentage: int = (block_count / infos.total_blocks * 100) if infos.total_blocks > 0 else 0

                result += f"{i}. {name}\n"
                result += f"   Blocs: {block_count:,} ({percentage:.2f}%)"
            result += f"\nTotal blocs: {infos.total_blocks:,}"

            return result

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    @property
    def get_mining_pool_hashrates(self) -> Optional[str]:
        """
        Récupère les hashrates du top 10 des mining pools sur 3 mois.

        Returns:
            str: Hashrates formatés ou None en cas d'erreur
        """
        try:
            data: dict = self.mempool.get_mining_pools_hashrate()
            if not data:
                return None

            infos: HashratesMiningPools = HashratesMiningPools.from_data(data)

            result: str = "=== Hashrates Mining Pools (3 mois) ===\n"

            for i, pool in enumerate(infos.pools, 1):
                pool_id: int = pool['id']
                hashrate_eh: int = pool['hashrate'] / 1_000_000_000_000_000_000  # EH/s
                share: int = pool['share'] * 100

                result += f"{i}. Pool #{pool_id}\n"
                result += f"   Hashrate: {hashrate_eh:.2f} EH/s\n"
                result += f"   Part du réseau: {share:.2f}%"

            return str(result)

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_top_pool(self) -> Optional[str]:
        """
        Récupère les infos du pool de mining #1.

        Returns:
            str: Infos du premier pool ou None en cas d'erreur
        """
        try:
            pools: dict = self.mempool.get_mining_pools_rank()
            if not pools:
                return None

            infos: TopMiningPool = TopMiningPool.from_data(pools)

            result: str = (
                f"=== Pool #1 ===\n"
                f"Nom: {infos.name}\n"
                f"Slug: {infos.slug}\n"
                f"Blocs minés (3 mois): {infos.block_count:,}\n"
                f"Pourcentage de tout les blocs miné (3 mois): {infos.percentage:.2f}%\n"
                f"Lien: {infos.link}\n"
            )
            return result

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_pool_by_slug(self, pool_slug: str) -> Optional[str]:
        """
        Recherche un mining pool spécifique par son nom.

        Args:
            pool_slug: Nom du pool recherché

        Returns:
            str: Infos du pool ou None si non trouvé/erreur
        """
        try:
            pool: dict = self.mempool.get_mining_pool_info_by_slug(pool_slug.lower())
            if not pool:
                return None

            infos: MiningPoolBySlug = MiningPoolBySlug.from_data(pool)

            # TODO : faire avec l'IA
            result = (
                f"=== {name} ===\n"
                f"Classement: #{rank}\n"
                f"Blocs minés (3 mois): {block_count:,}\n"
                f"Part du réseau: {percentage:.2f}%"
            )
            return result

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


    def get_mining_statistics(self) -> Optional[str]:
        """
        Récupère des statistiques générales sur le mining.

        Returns:
            str: Statistiques de mining ou None en cas d'erreur
        """
        try:
            data: dict = self.mempool.get_mining_pools_rank()
            if not data:
                return None

            infos: RankingMiningPools = RankingMiningPools.from_data(data)

            num_pools = len(infos.pools)
            avg_blocks_per_pool = infos.total_blocks / num_pools if num_pools > 0 else 0

            # Pool le plus actif
            top_pool = max(infos.pools, key=lambda x: x.get('blockCount', 0))
            top_pool_name = top_pool.get('name', 'Unknown')
            top_pool_blocks = top_pool.get('blockCount', 0)

            # Pool le moins actif
            bottom_pool = min(infos.pools, key=lambda x: x.get('blockCount', 0))
            bottom_pool_blocks = bottom_pool.get('blockCount', 0)

            result = (
                f"=== Statistiques Mining (3 mois) ===\n"
                f"Nombre de pools: {num_pools}\n"
                f"Total blocs minés: {infos.total_blocks:,}\n"
                f"Moyenne par pool: {avg_blocks_per_pool:.0f} blocs\n"
                f"\n🏆 Pool #1: {top_pool_name} ({top_pool_blocks:,} blocs)\n"
                f"📉 Pool le moins actif: {bottom_pool_blocks:,} blocs"
            )
            return result

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None