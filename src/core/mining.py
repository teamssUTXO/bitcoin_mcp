from typing import Optional

from src.api.mempool_client import get_mempool_client

from src.data.mining_dataclasses import DataRankingMiningPools, DataHashratesMiningPools, DataMiningPoolBySlug


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
            data: dict = self.mempool.get_mining_pools_rank()
            if not data:
                return None

            infos: DataRankingMiningPools = DataRankingMiningPools.from_data(data)

            total_blocks = sum(p.get("blockCount", 0) for p in infos.top10_pools)

            result: str = "## Top Mining Pools (3-Month Hashrate)\n"

            for i, pool in enumerate(infos.top10_pools, 1):
                name: str = pool.get('name', 'Unknown')
                block_count: int = pool.get('blockCount', 0)
                percentage: int = (block_count / total_blocks * 100) if total_blocks > 0 else 0

                result += f"#{i} {name}\n"
                result += f"Blocks: {block_count} ({percentage:.2f}%)\n"
            result += f"\nTotal Blocks: {total_blocks}\n"

            return result

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_mining_pool_hashrates(self) -> Optional[str]:
        """
        Récupère les hashrates du top 10 des mining pools sur 3 mois.

        Returns:
            str: Hashrates formatés ou None en cas d'erreur
        """
        try:
            data: list = self.mempool.get_mining_pools_hashrate()
            if not data:
                return None

            infos: DataHashratesMiningPools = DataHashratesMiningPools.from_data(data)

            result: str = "=== Hashrates Mining Pools (3 mois) ===\n"

            for i, pool in enumerate(infos.pools, 1):
                pool_name: str = pool.get('poolName', "")
                hashrate: int = pool.get('avgHashrate', 0)
                if hashrate > 0:
                    hashrate: float = hashrate / 1_000_000_000_000_000_000  # EH/s
                share: float = (pool.get('share', 0))
                if share > 0:
                    share *= 100

                result += f"#{i} {pool_name}\n"
                result += f"Hashrate: {hashrate:.2f} EH/s | Network Share: {share:.2f}%\n"

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
            data: dict = self.mempool.get_mining_pools_rank()
            if not data:
                return None

            infos: DataRankingMiningPools = DataRankingMiningPools.from_data(data)

            top_pool: dict = infos.pools[0]

            top_pool_name: str = top_pool.get('name', 'Unknown')
            top_pool_slug: str = top_pool.get('slug', 'Unknown')
            top_pool_block_count: int = top_pool.get('blockCount', 0)
            top_pool_link: str = top_pool.get('link', "")

            total_blocks: int = sum(p.get('blockCount', 0) for p in infos.pools)
            dominance_percentage: float = (top_pool_block_count / total_blocks * 100) if total_blocks > 0 else 0

            result: str = (
                f"## Top Mining Pool\n"
                f"Name: {top_pool_name}\n"
                f"Slug: {top_pool_slug}\n"
                f"Blocks Mined (3-Month): {top_pool_block_count}\n"
                f"Network Dominance: {dominance_percentage:.2f}%\n"
                f"Link: {top_pool_link}\n"
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
            data: dict = self.mempool.get_mining_pool_info_by_slug(pool_slug.lower())
            if not data:
                return None

            infos: DataMiningPoolBySlug = DataMiningPoolBySlug.from_data(data)

            unit: str = "H/s"
            for u in ["H/s", "KH/s", "MH/s", "GH/s", "TH/s", "PH/s", "EH/s"]:
                if infos.hashrate < 1000:
                    break
                infos.hashrate /= 1000
                unit = u
            formatted_hashrate: str = f"{infos.hashrate:.2f} {unit}"

            if infos.addresses:
                addr_list: str = "\n".join([f"  - {addr}" for addr in infos.addresses])
            else:
                addr_list: str = "  - Aucune adresse listée"

            result: str = (
                f"## Mining Pool Details\n"
                f"Name: {infos.name}\n"
                f"Website: {infos.link}\n\n"
                f"## Technical Performance\n"
                f"Hashrate: {formatted_hashrate}\n\n"
                f"## Block Statistics\n"
                f"Blocks Found: {infos.block_count}\n"
                f"Network Share: {infos.block_share}\n\n"
                f"## Pool Addresses\n"
                f"{addr_list}"
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

            infos: DataRankingMiningPools = DataRankingMiningPools.from_data(data)

            num_pools: int = len(infos.pools)

            total_blocks: int = sum(p.get("blockCount", 0) for p in infos.pools)
            avg_blocks_per_pool: int = total_blocks / num_pools if num_pools > 0 else 0

            top_pool: dict = max(infos.pools, key=lambda x: x.get('blockCount', 0))
            top_pool_name: str = top_pool.get('name', 'Unknown')
            top_pool_blocks: int = top_pool.get('blockCount', 0)

            bottom_pool: dict = min(infos.pools, key=lambda x: x.get('blockCount', 0))
            bottom_pool_blocks: int = bottom_pool.get('blockCount', 0)

            dominance_percentage: int = (top_pool_blocks / total_blocks * 100) if total_blocks > 0 else 0

            result: str = (
                f"## Global Mining Statistics (Bitcoin)\n"
                f"Active Pools: {num_pools}\n"
                f"Total Blocks Mined: {total_blocks}\n"
                f"Average per Pool: {avg_blocks_per_pool:.2f}\n\n"
                f"## Network Dominance\n"
                f"Leader: {top_pool_name}\n"
                f"Blocks: {top_pool_blocks} | Dominance: {dominance_percentage:.2f}%\n\n"
                f"## Power Distribution\n"
                f"Smallest Pool: {bottom_pool_blocks} blocks\n"
                f"Leader/Average Ratio: {(top_pool_blocks / avg_blocks_per_pool):.1f}x\n"
            )

            return result

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


# Singleton instance for the analyzer
_mining_analyser_instance = None

def get_mining_analyser_client() -> MiningPoolAnalyzer:
    """Get or create the Mining Pool Analyzer client singleton instance."""
    global _mining_analyser_instance
    if _mining_analyser_instance is None:
        _mining_analyser_instance = MiningPoolAnalyzer()
    return _mining_analyser_instance