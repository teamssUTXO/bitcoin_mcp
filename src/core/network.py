from typing import Optional

from api.mempool_client import get_mempool_client
from src.api.blockchain_client import get_blockchain_client

from data.network_dataclasses import NetworkFees, NetworkStats

from src.config import Config

class NetworkAnalyzer:
    """Analyseur du réseau Bitcoin"""

    def __init__(self):
        """
        Initialise l'analyseur réseau.
        """
        self.mempool = get_mempool_client()
        self.blockchain = get_blockchain_client()

    def get_network_stats(self) -> Optional[str]:
        """
        Récupère les statistiques complètes du réseau Bitcoin.

        Returns:
            str: Statistiques réseau formatées ou None en cas d'erreur
        """
        try:
            data: dict = self.blockchain.get_network_stats()
            if not data:
                return None

            infos: NetworkStats = NetworkStats.from_data(data)

            result: str = (
                f"=== Statistiques Réseau Bitcoin ===\n"
                f"Prix marché: ${infos.market_price_usd:,.2f}\n"
                f"Hashrate: {infos.hash_rate / 1_000_000_000:.2f} TH/s\n"
                f"Difficulté: {infos.difficulty:,.0f}\n"
                f"Prochain ajustement: Bloc #{infos.nextretarget}\n"
                f"\n=== Blocs ===\n"
                f"Blocs minés (24h): {infos.n_blocks_mined}\n"
                f"Total blocs: {infos.n_blocks_total:,}\n"
                f"Temps entre blocs: {infos.minutes_between_blocks:.2f} min\n"
                f"Taille des blocs: {infos.blocks_size:,} bytes\n"
                f"\n=== Transactions ===\n"
                f"Transactions (24h): {infos.n_tx:,}\n"
                f"BTC envoyés (estimé): {infos.estimated_btc_sent:,.2f} BTC\n"
                f"Volume transactions: ${infos.estimated_transaction_volume_usd:,.0f}\n"
                f"\n=== Mining ===\n"
                f"BTC minés (24h): {infos.n_btc_mined / 100_000_000:.2f} BTC\n"
                f"Frais totaux: {infos.total_fees_btc / 100_000_000:.8f} BTC\n"
                f"Revenus mineurs: {infos.miners_revenue_btc:.2f} BTC (${infos.miners_revenue_usd:,.0f})\n"
                f"\n=== Supply ===\n"
                f"BTC en circulation: {infos.totalbc:,.2f} BTC"
            )
            return result

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


    def get_network_recommended_fees(self) -> Optional[str]:
        """
        Récupère les frais de transaction recommandés.

        Returns:
            str: Frais recommandés formatés ou None en cas d'erreur
        """
        try:
            fees: dict = self.mempool.get_recommended_fees()
            if not fees:
                return None

            tx_size = 250 # taille de transaction standard
            infos: NetworkFees = NetworkFees.from_data(fees)

            costs: dict = {
                'Rapide (~10 min)': (infos.fastest * tx_size) / Config.SATOSHI,
                'Demi-heure': (infos.half_hour * tx_size) / Config.SATOSHI,
                'Standard (~1h)': (infos.hour * tx_size) / Config.SATOSHI,
                'Économique': (infos.economy * tx_size) / Config.SATOSHI
            }

            result: str = (
                f"=== Frais Recommandés (sat/vB) ===\n"
                f"Plus rapide: {infos.fastest} sat/vB (~10 min); (~{list(costs.values())[0]} BTC)\n"
                f"Demi-heure: {infos.half_hour} sat/vB (~30 min) (~{list(costs.values())[1]} BTC)\n"
                f"Une heure: {infos.hour} sat/vB (~60 min) (~{list(costs.values())[2]} BTC)\n"
                f"Économique: {infos.economy} sat/vB (~{list(costs.values())[3]} BTC)\n"
                f"Minimum: {infos.minimum} sat/vB (~{list(costs.values())[4]} BTC)"
            )

            return result


        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


    def get_network_health(self) -> Optional[str]:
        """
        Évalue la santé globale du réseau Bitcoin.

        Returns:
            str: Analyse de santé du réseau ou None en cas d'erreur
        """
        try:
            stats: dict = self.blockchain.get_network_stats()
            if not stats:
                return None

            infos: NetworkStats = NetworkStats.from_data(stats)

            # Évaluation de la santé
            health_score: int = 100
            issues: list = []

            # Temps entre blocs (optimal: ~10 min)
            if infos.minutes_between_blocks > 15:
                health_score -= 20
                issues.append(f"Blocs lents ({infos.minutes_between_blocks:.1f} min)")
            elif infos.minutes_between_blocks < 5:
                health_score -= 10
                issues.append(f"Blocs rapides ({infos.minutes_between_blocks:.1f} min)")

            # Hashrate (doit être élevé pour la sécurité)
            if infos.hash_rate < 100_000_000_000:  # < 100 TH/s
                health_score -= 30
                issues.append("Hashrate faible")

            # Volume de transactions
            if infos.n_tx < 100_000:
                health_score -= 15
                issues.append("Faible volume de transactions")

            status: str = "Excellent" if health_score >= 90 else \
                "Bon" if health_score >= 70 else \
                    "Moyen" if health_score >= 50 else "Faible"

            result: str = f"État du réseau: {status} ({health_score}/100)\n"
            if issues:
                result += "Points d'attention: " + ", ".join(issues)
            else:
                result += "Aucun problème détecté"

            return result

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None
