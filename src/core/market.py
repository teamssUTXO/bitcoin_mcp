from typing import Optional

from src.data.market_dataclasses import BitcoinOverview, BitcoinMarket, BitcoinMarketSentiment
from src.data.market_dataclasses import MarketOverview

from src.api.coingecko_client import get_coingecko_client
from src.api.alternative_client import get_alternative_client


class MarketAnalyzer:
    """Analyseur du marché crypto"""

    def __init__(self):
        """
        Initialise l'analyseur de marché.
        """
        self.coingecko = get_coingecko_client()
        self.alternative = get_alternative_client()

    def get_global_cryptomarket_data(self) -> Optional[str]:
        """
        Récupère les données globales du marché des cryptos puis les formates

        Returns:
            str: Données formatées du marché global ou None en cas d'erreur
        """
        try:
            data: dict = self.coingecko.get_global_market_data()
            if not data:
                return None

            infos: MarketOverview = MarketOverview.from_data(data)

            # TODO: faire le return par IA
            result: str = ( ""
                # f"Capitalisation totale: ${infos.nb_markets:,.0f}\n"
                # f"Volume 24h: ${infos.volume_24h:,.0f}\n"
                # f"Dominance BTC: {infos.btc_dominance:.2f}%\n"
                # f"Cryptos actives: {infos.active_cryptos}"
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
            data: dict = self.coingecko.get_btc_price_usd()
            if not data:
                return None

            infos: BitcoinOverview = BitcoinOverview.from_data(data)

            # TODO: faire le return par IA
            result: str = ( ""
                # f"Prix BTC: ${infos.usd:,.2f} USD"
                # f"Capitalisation totale: ${infos.market_cap:,.0f}\n"
                # f"Volume 24h: ${infos.volume_24h:,.0f}\n"
                # f"Dominance BTC: {infos.btc_dominance:.2f}%\n"
                # f"Cryptos actives: {infos.active_cryptos}"
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
            data: dict = self.coingecko.get_btc_market_data()
            if not data:
                return None

            infos: BitcoinMarket = BitcoinMarket.from_data(data)

            # TODO: faire le return par IA
            result: str = ( ""
                # f"Bitcoin (btc)\n"
                # f"Prix actuel: ${infos.current_price:,.2f}\n"
                # f"Capitalisation: ${infos.market_cap:,.0f}\n"
                # f"Volume 24h: ${infos.volume_24h:,.0f}\n"
                # f"Variation 24h: {infos.price_change_24h:+.2f}%\n"
                # f"ATH: ${infos.ath_price:,.2f} | ATL: ${infos.atl_price:,.2f}"
            )
            return result

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


    def get_market_sentiment(self) -> Optional[str]:
        """
        Analyse le sentiment de marché.

        Returns:
            str: Analyse de sentiment ou None en cas d'erreur
        """
        try:
            alternative_data: dict = self.alternative.get_fear_greed_index()
            coingecko_data: dict = self.coingecko.get_btc_market_data()
            if not alternative_data | coingecko_data:
                return None

            infos: BitcoinMarketSentiment = BitcoinMarketSentiment.from_data(alternative_data, coingecko_data)

            # Définit : fg_data_1, 2, 3... = [valeur de l'indice fg du jour, classification de cet index]
            for i in range(1, 8):
                setattr(self, f"fg_data_{i}d",
                        [
                            infos.fg_data[i]["value"],
                            infos.fg_data[i]["value_classification"]
                        ]
                        )

            # TODO: à faire avec l'IA
            result: str = ( ""
                # f"Market Sentiment (lastest 7 days):\n"
                # f"Prix actuel: ${infos.current_price:,.2f}\n"
                # f"Capitalisation: ${infos.market_cap:,.0f}\n"
                # f"Volume 24h: ${infos.volume_24h:,.0f}\n"
                # f"Variation 24h: {infos.price_change_24h:+.2f}%\n"
                # f"ATH: ${infos.ath_price:,.2f} | ATL: ${infos.atl_price:,.2f}"
            )

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None