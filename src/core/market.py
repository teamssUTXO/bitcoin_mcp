from typing import Optional

from src.api.coingecko_client import get_coingecko_client
from src.api.alternative_client import get_alternative_client

from src.data.market_dataclasses import DataMarketOverview, DataBitcoinOverview, DataBitcoinMarket, \
    DataBitcoinMarketSentiment, DataTrendingCategories, DataTrendingCoins, DataTrendingNFTs


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
        Récupère les données globales du marché des cryptos puis les formate

        Returns:
            str: Données formatées du marché global ou None en cas d'erreur
        """
        try:
            data: dict = self.coingecko.get_global_market_data()
            if not data:
                return None

            infos: DataMarketOverview = DataMarketOverview.from_data(data)

            fmt_cap = "\n".join([f"  - {k}: {v:,.0f}" for k, v in infos.five_biggest_market_cap.items()])
            fmt_vol = "\n".join([f"  - {k}: {v:,.0f}" for k, v in infos.five_biggest_market_volume.items()])
            fmt_dom = "\n".join([f"  - {k}: {v:.2f}%" for k, v in infos.five_biggest_market_cap_percentage.items()])

            result: str = (
                f"=== Vue d'ensemble du Marché ===\n"
                f"Cryptos actives : {infos.active_cryptocurrencies:,}\n"
                f"Nombre de marchés : {infos.nb_markets:,}\n"
                f"Variation globale (Market Cap) : {infos.market_cap_change_percentage:+.2f}%\n\n"
                f"--- État des ICOs ---\n"
                f"• À venir : {infos.upcoming_icos}\n"
                f"• En cours : {infos.ongoing_icos}\n"
                f"• Terminées : {infos.ended_icos}\n\n"
                f"--- Top 5 Market Cap ---\n"
                f"{fmt_cap}\n\n"
                f"--- Top 5 Volume ---\n"
                f"{fmt_vol}\n\n"
                f"--- Dominance (Parts de marché) ---\n"
                f"{fmt_dom}\n"
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

            infos: DataBitcoinOverview = DataBitcoinOverview.from_data(data)

            circulating_supply = infos.usd_market_cap / infos.usd if infos.usd else 0
            vol_cap_ratio = (infos.usd_24h_vol / infos.usd_market_cap) * 100 if infos.usd_market_cap else 0
            price_yesterday = infos.usd / (1 + (infos.usd_24h_change / 100))


            result: str = (
                f"=== Données du Marché (USD) ===\n"
                f"Prix actuel: ${infos.usd:,.2f}\n"
                f"Prix hier (est.): ${price_yesterday:,.2f}\n"
                f"Variation sur 24h: {infos.usd_24h_change:+.2f}%\n"
                f"\n"
                f"--- Indicateurs Calculés ---\n"
                f"Capitalisation: ${infos.usd_market_cap:,.0f}\n"
                f"Volume 24h: ${infos.usd_24h_vol:,.0f}\n"
                f"Ratio Vol/Cap: {vol_cap_ratio:.2f}% (Liquidité)\n"
                f"Offre en circulation: {circulating_supply:,.0f} jetons\n"
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

            infos: DataBitcoinMarket = DataBitcoinMarket.from_data(data)

            if infos.max_supply and infos.max_supply > 0:
                supply_minted_pct = (infos.total_supply / infos.max_supply) * 100
                fdv = infos.max_supply * infos.current_price
                supply_info = f"{supply_minted_pct:.2f}% minés sur {infos.max_supply:,.0f}"
                fdv_info = f"${fdv:,.0f}"
            else:
                supply_info = "Offre illimitée ou inconnue"
                fdv_info = "N/A"

            volatility_gap = infos.high_price_24h - infos.low_price_24h
            volatility_pct = (volatility_gap / infos.low_price_24h * 100) if infos.low_price_24h else 0
            short_desc = (infos.description[:150] + '...') if len(infos.description) > 150 else infos.description

            result: str = (
                f"=== Rapport Technique & Financier (Rang #{infos.market_cap_rank}) ===\n"
                f"Prix Actuel: ${infos.current_price:,.4f}\n"
                f"Capitalisation (MC): ${infos.market_cap:,.0f}\n"
                f"Date de création (Genesis): {infos.genesis_date}\n\n"

                f"--- Tokenomics & Offre ---\n"
                f"Total Supply: {infos.total_supply:,.0f}\n"
                f"Max Supply: {supply_info}\n"
                f"FDV (Fully Diluted): {fdv_info}\n"
                f"Algo / Block Time: {infos.hashing_algorithm} ({infos.block_time_in_minutes} min)\n\n"

                f"--- Volatilité & Bornes (24h) ---\n"
                f"Plus Haut (High): ${infos.high_price_24h:,.4f}\n"
                f"Plus Bas (Low): ${infos.low_price_24h:,.4f}\n"
                f"Écart (Volatilité): {volatility_pct:.2f}% (${volatility_gap:,.4f})\n\n"

                f"--- Performance Historique (ATH/ATL) ---\n"
                f"• ATH (Record): ${infos.ath_price:,.4f} le {infos.ath_date[:10]}\n"
                f"  Chute depuis ATH: {infos.ath_change_percentage:.2f}%\n"
                f"• ATL (Plancher): ${infos.atl_price:,.4f} le {infos.atl_date[:10]}\n"
                f"  Hausse depuis ATL: {infos.atl_change_percentage:+.2f}%\n\n"

                f"--- Analyse Temporelle (Tendance) ---\n"
                f"Période | Variation % | Prix Précédent\n"
                f"--------|-------------|---------------\n"
                f"1H      | {infos.price_change_percentage_1h:>+7.2f}%    | ${infos.price_1h_before:,.4f}\n"
                f"24H     | {infos.price_change_percentage_24h:>+7.2f}%    | ${infos.price_24h_before:,.4f}\n"
                f"7J      | {infos.price_change_percentage_7d:>+7.2f}%    | ${infos.price_7d_before:,.4f}\n"
                f"30J     | {infos.price_change_percentage_30d:>+7.2f}%    | ${infos.price_30d_before:,.4f}\n"
                f"60J     | {infos.price_change_percentage_60d:>+7.2f}%    | ${infos.price_60d_before:,.4f}\n"
                f"1 AN    | {infos.price_change_percentage_1y:>+7.2f}%    | ${infos.price_1y_before:,.4f}\n\n"

                f"--- Informations & Liens ---\n"
                f"GitHub: {infos.repo_github_link}\n"
                f"Whitepaper: {infos.white_paper_link}\n"
                f"Description: {short_desc}\n"
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

            infos: DataBitcoinMarketSentiment = DataBitcoinMarketSentiment.from_data(alternative_data, coingecko_data)

            # Définit : fg_data_1, 2, 3... = [valeur de l'indice fg du jour, classification de cet index]
            fg_lines = []
            for i in range(1, 8):
                day_data = getattr(infos, f"fg_data_{i}d", ["N/A", "Inconnu"])
                fg_lines.append(f"  J-{i}: {day_data[0]} - {day_data[1]}")
            fg_history_txt = "\n".join(fg_lines)

            sentiment_label = "Neutre"
            if infos.sentiment_votes_up_percentage > infos.sentiment_votes_down_percentage:
                sentiment_label = "🟢 Majorité Haussière (Bullish)"
            elif infos.sentiment_votes_down_percentage > infos.sentiment_votes_up_percentage:
                sentiment_label = "🔴 Majorité Baissière (Bearish)"

            result: str = (
                f"=== Psychologie & Sentiment du Marché ===\n"
                f"--- Sentiment Communautaire (CoinGecko) ---\n"
                f"Tendance: {sentiment_label}\n"
                f"👍 Optimistes (Votes Up): {infos.sentiment_votes_up_percentage:.0f}%\n"
                f"👎 Pessimistes (Votes Down): {infos.sentiment_votes_down_percentage:.0f}%\n"
                f"\n"
                f"--- Historique Fear & Greed (7 derniers jours) ---\n"
                f"Indicateur de peur et d'avidité (Source: Alternative.me)\n"
                f"{fg_history_txt}\n"
            )

            return result

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


    def get_trending_coins(self) -> Optional[str]:
        """
        Recupère les coins en tendance

        Returns:
            str: Coins en tendance
        """
        try:
            data: dict = self.coingecko.get_market_trend()
            if not data:
                return None

            infos: DataTrendingCoins = DataTrendingCoins.from_data(data)

            result: list = ["=== Trending Coins ==="]

            for i in range(len(data.get("coins", []))):
                result.append(
                    f"=== Coin {infos.names[i]} / {infos.symbols[i]} ===\n"
                    f"Rank (Trending): {infos.ranks[i]}\n"
                    f"Price: {infos.prices[i]:.8f} USD\n"
                    f"Price 24h (yesterday): {(infos.prices[i] / (1 + (infos.prices_changed[i] / 100))):.2f} : {infos.prices_changed[i]:.2f}%\n"
                    f"Market Cap: {infos.market_caps[i]} USD\n"
                    f"Market Cap Rank: {infos.market_cap_ranks[i]}\n"
                    f"Total Volume: {infos.total_volumes[i]} USD\n"
                    f"\nDescription:\n{infos.descriptions[i]}\n"
                )

            return "\n".join(result)

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_trending_categories(self) -> Optional[str]:
        """
        Recupère les categories de cryptomonnaies en tendance

        Returns:
            str: Categories en tendance
        """
        try:
            data: dict = self.coingecko.get_market_trend()
            if not data:
                return None

            infos: DataTrendingCategories = DataTrendingCategories.from_data(data)

            result: list = ["=== Trending Categories ==="]

            for i in range(len(data.get("categories", []))):
                result.append(
                    f"=== Categorie Top {i+1} {infos.names[i]} ===\n"
                    f"Number of Coins : {infos.n_coins_count[i]}\n"
                    f"Market Cap: {infos.market_caps[i]} USD\n"
                    f"market Cap 24h (yesterday): {(infos.market_caps[i] / (1 + (infos.market_caps_changed[i] / 100))):.2f} : {infos.market_caps_changed[i]:.2f}%\n"
                    f"Total Volume: {infos.total_volumes[i]} USD\n"
                )

            return "\n".join(result)

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None

    def get_trending_nfts(self) -> Optional[str]:
        """
        Recupère les nfts en tendance

        Returns:
            str: nfts en tendance
        """
        try:
            data: dict = self.coingecko.get_market_trend()
            if not data:
                return None

            infos: DataTrendingNFTs = DataTrendingNFTs.from_data(data)

            result: list = ["=== Trending NFTs ==="]

            for i in range(len(data.get("nfts", []))):
                result.append(
                    f"=== NFT {infos.names[i]} : {infos.symbols[i]} ===\n"
                    f"Rank : {i+1}\n"
                    f"Currency : {infos.native_currencies[i]}\n"
                    f"Floor price: {infos.floor_prices[i]}\n"
                    f"24h Change: {infos.floor_prices_24h_percentage_change[i]}%\n"
                    f"24h Volume: {infos.h24_volumes[i]}\n"
                    f"Average sale (24h): {infos.h24_avg_sell_price[i]}\n"
                )

            return "\n".join(result)

        except KeyError as e:
            print(f"Erreur type: 02 - Clé manquante: {e}")
            return None
        except Exception as e:
            print(f"Erreur API: 01 - {e}")
            return None


# Singleton instance for the analyzer
_market_analyser_instance = None

def get_market_analyser_client() -> MarketAnalyzer:
    """Get or create the Market Analyzer client singleton instance."""
    global _market_analyser_instance
    if _market_analyser_instance is None:
        _market_analyser_instance = MarketAnalyzer()
    return _market_analyser_instance