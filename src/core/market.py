from typing import Optional

from data.market_dataclasses import BitcoinOverview, BitcoinMarket
from src.api.coingecko_client import CoinGeckoClient
from src.api.alternative_client import AlternativeClient

from src.data.market_dataclasses import MarketOverview

# TODO: voir en bas

class MarketAnalyzer:
    """Analyseur du marché crypto"""

    def __init__(self):
        """
        Initialise l'analyseur de marché.
        """
        self.coingecko = CoinGeckoClient()
        self.alternative = AlternativeClient()

    def get_global_market_data(self) -> Optional[str]:
        """
        Récupère les données globales du marché des cryptos puis les formates

        Returns:
            str: Données formatées du marché global ou None en cas d'erreur
        """
        try:
            data = self.coingecko.get_global_market_data()
            if not data:
                return None

            infos = MarketOverview.from_data(data)

            # TODO: faire le return par IA
            result = (
                f"Capitalisation totale: ${infos["market_cap"]:,.0f}\n"
                f"Volume 24h: ${infos["volume_24h"]:,.0f}\n"
                f"Dominance BTC: {infos["btc_dominance"]:.2f}%\n"
                f"Cryptos actives: {infos["active_cryptos"]}"
            )
            return result

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_btc_price_usd(self) -> Optional[str]:
        """
        Récupère le prix actuel du Bitcoin en USD.

        Returns:
            str: Prix formaté du BTC ou None en cas d'erreur
        """
        try:
            data = self.coingecko.get_btc_price_usd()
            if not data:
                return None

            infos = BitcoinOverview.from_data(data)

            # TODO: faire le return par IA
            result = (
                f"Prix BTC: ${infos.usd:,.2f} USD"
                f"Capitalisation totale: ${infos.market_cap:,.0f}\n"
                f"Volume 24h: ${infos.volume_24h:,.0f}\n"
                f"Dominance BTC: {infos.btc_dominance:.2f}%\n"
                f"Cryptos actives: {infos.active_cryptos}"
            )
            return result

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_btc_market_data(self) -> Optional[str]:
        """
        Récupère les informations détaillées sur le marché Bitcoin.

        Returns:
            str: Données de marché formatées ou None en cas d'erreur
        """
        try:
            data = self.coingecko.get_btc_market_data()
            if not data:
                return None

            infos = BitcoinMarket.from_data(data)

            # TODO: faire le return par IA
            result = (
                f"Bitcoin (btc)\n"
                f"Prix actuel: ${infos.current_price:,.2f}\n"
                f"Capitalisation: ${infos.market_cap:,.0f}\n"
                f"Volume 24h: ${infos.volume_24h:,.0f}\n"
                f"Variation 24h: {infos.price_change_24h:+.2f}%\n"
                f"ATH: ${infos.ath_price:,.2f} | ATL: ${infos.atl_price:,.2f}"
            )
            return result

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_global_cryptomarket_infos(self) -> Optional[str]:
        """
        Récupère les informations globales sur le marché crypto (Alternative.me).

        Returns:
            str: Informations de marché formatées ou None en cas d'erreur
        """
        try:
            data = self.alternative.get_global_cryptomarket_infos()
            if not data:
                return None

            # Alternative.me renvoie des statistiques générales
            # Structure exacte à vérifier selon l'API
            result_data = data.get('data', {})

            # Formater selon les données disponibles
            if isinstance(result_data, list) and len(result_data) > 0:
                info = result_data[0]
                return f"Marché crypto global: {info}"

            return str(result_data)

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_fear_greed_index(self) -> Optional[str]:
        """
        Récupère l'indice Fear & Greed sur 7 jours.

        Returns:
            str: Indice F&G formaté ou None en cas d'erreur
        """
        try:
            data = self.alternative.get_fear_greed_index()
            if not data:
                return None

            # L'API retourne un tableau de données sur plusieurs jours
            data_list = data.get('data', [])
            if not data_list:
                print("Erreur type: 02 - Données vides")
                return None

            # Formater les 7 derniers jours
            result_lines = ["Indice Fear & Greed (7 derniers jours):"]
            for entry in data_list[:7]:
                value = entry.get('value', 'N/A')
                classification = entry.get('value_classification', 'N/A')
                timestamp = entry.get('timestamp', 'N/A')

                result_lines.append(f"  - {timestamp}: {value} ({classification})")

            return "\n".join(result_lines)

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_market_sentiment(self) -> Optional[str]:
        """
        Analyse le sentiment de marché combiné (Fear & Greed + variation de prix).

        Returns:
            str: Analyse de sentiment ou None en cas d'erreur
        """
        try:
            # Récupérer l'indice Fear & Greed actuel
            fg_data = self.alternative.get_fear_greed_index()
            btc_price_data = self.coingecko.get_market_data()

            if not fg_data or not btc_price_data:
                return None

            fg_value = int(fg_data.get('data', [{}])[0].get('value', 50))
            fg_class = fg_data.get('data', [{}])[0].get('value_classification', 'Neutral')

            price_change = btc_price_data.get('market_data', {}).get('price_change_percentage_24h', 0)

            sentiment = "neutre"
            if fg_value < 25:
                sentiment = "très craintif"
            elif fg_value < 45:
                sentiment = "craintif"
            elif fg_value > 75:
                sentiment = "très avide"
            elif fg_value > 55:
                sentiment = "avide"

            result = (
                f"Sentiment du marché: {sentiment}\n"
                f"Indice F&G: {fg_value}/100 ({fg_class})\n"
                f"Variation BTC 24h: {price_change:+.2f}%"
            )
            return result

        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None