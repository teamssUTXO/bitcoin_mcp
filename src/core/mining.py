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

            result: str = "=== Top Mining Pools (3 mois) ===\n"

            for i, pool in enumerate(infos.top10_pools, 1):
                name: str = pool.get('name', 'Unknown')
                block_count: int = pool.get('blockCount', 0)
                percentage: int = (block_count / total_blocks * 100) if total_blocks > 0 else 0

                result += f"{i}. {name}\n"
                result += f"   Blocs: {block_count:,} ({percentage:.2f}%)"
            result += f"\nTotal blocs: {total_blocks:,}"

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
                pool_id: int = pool.get('id', 0)
                hashrate: int = pool.get('hashrate', 0)
                if hashrate > 0:
                    hashrate: float = hashrate / 1_000_000_000_000_000_000  # EH/s
                share: float = (pool.get('share', 0))
                if share > 0:
                    share *= 100

                result += f"{i}. Pool #{pool_id}\n"
                result += f"   Hashrate: {hashrate:.2f} EH/s\n"
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
            dominance_percentage = (top_pool_block_count / total_blocks * 100) if total_blocks > 0 else 0

            result: str = (
                f"=== Pool #1 ===\n"
                f"Nom: {top_pool_name}\n"
                f"Slug: {top_pool_slug}\n"
                f"Blocs minés (3 mois): {top_pool_block_count:,}\n"
                f"Pourcentage de tout les blocs miné (3 mois): {dominance_percentage:.2f}%\n"
                f"Lien: {top_pool_link}\n"
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


            hr = infos.hashrate
            unit = "H/s"
            for u in ["H/s", "KH/s", "MH/s", "GH/s", "TH/s", "PH/s", "EH/s"]:
                if hr < 1000:
                    break
                hr /= 1000
                unit = u
            formatted_hashrate = f"{hr:.2f} {unit}"

            if infos.addresses:
                addr_list = "\n".join([f"  - {addr}" for addr in infos.addresses])
            else:
                addr_list = "  - Aucune adresse listée"

            result: str = (
                f"=== Détails du Pool de Minage ===\n"
                f"Nom: {infos.name}\n"
                f"Site Web: {infos.link}\n"
                f"\n"
                f"--- Performance Technique ---\n"
                f"Puissance (Hashrate): {formatted_hashrate}\n"
                f"\n"
                f"--- Statistiques de Blocs ---\n"
                f"Nombre de blocs trouvés :\n"
                f"{infos.block_count}\n"
                f"\n"
                f"Part du réseau (Block Share) :\n"
                f"{infos.block_share}\n"
                f"\n"
                f"--- Adresses du Pool ---\n"
                f"{addr_list}\n"
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

            num_pools = len(infos.pools)

            total_blocks = sum(p.get("blockCount", 0) for p in infos.pools)
            avg_blocks_per_pool = total_blocks / num_pools if num_pools > 0 else 0

            top_pool = max(infos.pools, key=lambda x: x.get('blockCount', 0))
            top_pool_name = top_pool.get('name', 'Unknown')
            top_pool_blocks = top_pool.get('blockCount', 0)

            bottom_pool = min(infos.pools, key=lambda x: x.get('blockCount', 0))
            bottom_pool_blocks = bottom_pool.get('blockCount', 0)

            dominance_percentage = (top_pool_blocks / total_blocks * 100) if total_blocks > 0 else 0

            result: str = (
                f"=== Statistiques Globales du Minage (Bitcoin) ===\n"
                f"Pools actifs recensés : {num_pools}\n"
                f"Total de blocs minés : {total_blocks:,}\n"
                f"Moyenne par pool : {avg_blocks_per_pool:,.2f} blocs\n"
                f"\n"
                f"--- Dominance du Réseau ---\n"
                f"🏆 Leader actuel : {top_pool_name}\n"
                f"   Volume : {top_pool_blocks:,} blocs\n"
                f"   Dominance : {dominance_percentage:.2f}% du réseau\n"
                f"\n"
                f"--- Écart de Puissance ---\n"
                f"Plus petit acteur : {bottom_pool_blocks} bloc(s)\n"
                f"Ratio Leader/Moyenne : x{(top_pool_blocks / avg_blocks_per_pool):.1f}\n"
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