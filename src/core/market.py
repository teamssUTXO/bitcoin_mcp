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

            market_cap: dict = {"usd": infos.data.get("total_market_cap", {}).get("usd", {}),
                                     "eur": infos.data.get("total_market_cap", {}).get("eur", {}),
                                     "btc": infos.data.get("total_market_cap", {}).get("btc", {}),
                                    "eth": infos.data.get("total_market_cap", {}).get("eth", {})}

            market_volume: dict = {"usd": infos.data.get("total_volume", {}).get("usd", {}),
                                "eur": infos.data.get("total_volume", {}).get("eur", {}),
                                "btc": infos.data.get("total_volume", {}).get("btc", {}),
                                "eth": infos.data.get("total_volume", {}).get("eth", {})}

            five_biggest_market_cap_percentage: dict = dict(list(infos.market_cap_percentage.items())[:5])

            fmt_cap: str = "\n".join([f"  - {k}: {v:,.0f}" for k, v in market_cap.items()])
            fmt_vol: str = "\n".join([f"  - {k}: {v:,.0f}" for k, v in market_volume.items()])
            fmt_dom: str = "\n".join([f"  - {k}: {v:.2f}%" for k, v in five_biggest_market_cap_percentage.items()])

            result: str = (
                f"## Crypto Market Overview\n"
                f"Active Cryptocurrencies: {infos.active_cryptocurrencies}\n"
                f"Markets: {infos.nb_markets}\n"
                f"Market Cap Change: {infos.market_cap_change_percentage:+.2f}%\n\n"
                f"## ICO Status\n"
                f"Upcoming: {infos.upcoming_icos}\n"
                f"Ongoing: {infos.ongoing_icos}\n"
                f"Ended: {infos.ended_icos}\n\n"
                f"## Market Capitalization\n"
                f"{fmt_cap}\n\n"
                f"## Trading Volume\n"
                f"{fmt_vol}\n\n"
                f"## Top 5 Market Dominance\n"
                f"{fmt_dom}"
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

            circulating_supply: int = infos.usd_market_cap / infos.usd if infos.usd else 0
            vol_cap_ratio: int = (infos.usd_24h_vol / infos.usd_market_cap) * 100 if infos.usd_market_cap else 0
            price_yesterday: float = infos.usd / (1 + (infos.usd_24h_change / 100))

            result: str = (
                f"## Market Data (USD)\n"
                f"Current Price: ${infos.usd:,.2f}\n"
                f"Price 24h Ago: ${price_yesterday:,.2f}\n"
                f"24h Change: {infos.usd_24h_change:+.2f}%\n\n"
                f"## Market Indicators\n"
                f"Market Cap: ${infos.usd_market_cap:,.0f}\n"
                f"24h Volume: ${infos.usd_24h_vol:,.0f}\n"
                f"Vol/Cap Ratio: {vol_cap_ratio:.2f}%\n"
                f"Circulating Supply: {circulating_supply:,.0f} tokens"
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
                supply_minted_pct: float = (infos.total_supply / infos.max_supply) * 100
                fdv: int = infos.max_supply * infos.current_price
                supply_info: str = f"{supply_minted_pct:.2f}% minés sur {infos.max_supply:,.0f}"
                fdv_info: str = f"${fdv:,.0f}"
            else:
                supply_info: str = "Offre illimitée ou inconnue"
                fdv_info: str = "N/A"

            volatility_gap: int = infos.high_price_24h - infos.low_price_24h
            volatility_pct: int = (volatility_gap / infos.low_price_24h * 100) if infos.low_price_24h else 0

            result: str = (
                f"## Technical & Financial Report\n"
                f"Market Cap Rank: #{infos.market_cap_rank}\n"
                f"Current Price: ${infos.current_price:,.4f}\n"
                f"Market Cap: ${infos.market_cap:,.0f}\n"
                f"Genesis Date: {infos.genesis_date}\n\n"

                f"## Tokenomics\n"
                f"Total Supply: {infos.total_supply:,.0f}\n"
                f"Max Supply: {supply_info}\n"
                f"Fully Diluted Valuation: {fdv_info}\n"
                f"Algorithm: {infos.hashing_algorithm} | Block Time: {infos.block_time_in_minutes} min\n\n"

                f"## 24h Volatility\n"
                f"High: ${infos.high_price_24h:,.4f}\n"
                f"Low: ${infos.low_price_24h:,.4f}\n"
                f"Range: {volatility_pct:.2f}% (${volatility_gap:,.4f})\n\n"

                f"## Historical Performance\n"
                f"ATH: ${infos.ath_price:,.4f} on {infos.ath_date[:10]} | Change: {infos.ath_change_percentage:.2f}%\n"
                f"ATL: ${infos.atl_price:,.4f} on {infos.atl_date[:10]} | Change: {infos.atl_change_percentage:+.2f}%\n\n"

                f"## Price Change Analysis\n"
                f"Period | Change % | Previous Price\n"
                f"-------|----------|---------------\n"
                f"1h     | {infos.price_change_percentage_1h:>+7.2f}% | ${infos.price_1h_before:,.4f}\n"
                f"24h    | {infos.price_change_percentage_24h:>+7.2f}% | ${infos.price_24h_before:,.4f}\n"
                f"7d     | {infos.price_change_percentage_7d:>+7.2f}% | ${infos.price_7d_before:,.4f}\n"
                f"30d    | {infos.price_change_percentage_30d:>+7.2f}% | ${infos.price_30d_before:,.4f}\n"
                f"60d    | {infos.price_change_percentage_60d:>+7.2f}% | ${infos.price_60d_before:,.4f}\n"
                f"1y     | {infos.price_change_percentage_1y:>+7.2f}% | ${infos.price_1y_before:,.4f}\n\n"

                f"## Resources\n"
                f"GitHub: {infos.repo_github_link}\n"
                f"Whitepaper: {infos.white_paper_link}\n"
                f"Description: {infos.description}"
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
            fg_lines: list = []
            for i in range(1, 8):
                day_data: list = getattr(infos, f"fg_data_{i}d", ["N/A", "Inconnu"])
                fg_lines.append(f"  J-{i}: {day_data[0]} - {day_data[1]}")
            fg_history_txt: str = "\n".join(fg_lines)

            sentiment_label: str = "Neutre"
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
                    f"## {infos.names[i]} ({infos.symbols[i]})\n"
                    f"Trending Rank: {infos.ranks[i]}\n"
                    f"Price: ${infos.prices[i]:.8f}\n"
                    f"Price 24h Ago: ${(infos.prices[i] / (1 + (infos.prices_changed[i] / 100))):.8f} | Change: {infos.prices_changed[i]:+.2f}%\n"
                    f"Market Cap: ${infos.market_caps[i]} | Rank: {infos.market_cap_ranks[i]}\n"
                    f"24h Volume: ${infos.total_volumes[i]}\n\n"
                    f"Description: {infos.descriptions[i]}\n"
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
                    f"## Top {i + 1}: {infos.names[i]}\n"
                    f"Coins in Category: {infos.n_coins_count[i]}\n"
                    f"Market Cap: ${infos.market_caps[i]}\n"
                    f"Market Cap 24h Ago: ${(infos.market_caps[i] / (1 + (infos.market_caps_changed[i] / 100)))} | Change: {infos.market_caps_changed[i]:+.2f}%\n"
                    f"24h Volume: ${infos.total_volumes[i]}\n"
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
                    f"## NFT Top {i + 1}: {infos.names[i]} ({infos.symbols[i]})\n"
                    f"Currency: {infos.native_currencies[i]}\n"
                    f"Floor Price: {infos.floor_prices[i]} | 24h Change: {infos.floor_prices_24h_percentage_change[i]:+.2f}%\n"
                    f"24h Volume: {infos.h24_volumes[i]}\n"
                    f"24h Avg Sale: {infos.h24_avg_sell_price[i]}\n"
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