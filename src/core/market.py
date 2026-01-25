import logging
from typing import Optional

from src.api.coingecko_client import get_coingecko_client
from src.api.alternative_client import get_alternative_client

from src.data.market_dataclasses import DataMarketOverview, DataBitcoinOverview, DataBitcoinMarket, \
    DataBitcoinMarketSentiment, DataTrendingCategories, DataTrendingCoins, DataTrendingNFTs, DataBitcoinPriceUSD


logger = logging.getLogger(__name__)

class MarketAnalyzer:
    """Cryptocurrency Market Analyzer"""

    def __init__(self):
        """
        Initialize Cryptocurrency Market Analyzer.
        """
        self.coingecko = get_coingecko_client()
        self.alternative = get_alternative_client()

    def get_global_cryptomarket_data(self) -> Optional[str]:
        """
        Retrieves a global overview of the cryptocurrency market.

        Returns:
            A Markdown formatted string including:
            - General stats (Active cryptos, number of markets, market cap change).
            - ICO status (Upcoming, ongoing, and ended).
            - Total Market Capitalization and Volume (USD, EUR, BTC, ETH).
            - Top 5 Market Dominance percentages.
            Returns None if an API error occurs or data is missing.
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


        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None

    def get_btc_price_usd(self) -> Optional[str]:
        """
        Retrieves the current Bitcoin price in USD.

        Returns:
            A Markdown formatted string including:
            - Current Price data.
            Returns None if an API error occurs or data is missing.
        """
        try:
            data: dict = self.coingecko.get_btc_price_usd()
            if not data:
                return None

            infos: DataBitcoinPriceUSD = DataBitcoinPriceUSD.from_data(data)

            result: str = f"Current Bitcoin Price in USD: ${infos.price_usd:,.2f}"
            return result

        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None

    def get_btc_market_data(self) -> Optional[str]:
        """
        Retrieves a technical and financial report for Bitcoin.

        Returns:
            A Markdown formatted string including:
            - Market rankings and current valuation (Price, Cap, Rank).
            - Tokenomics (Supply, FDV, Algorithm, and Block time).
            - 24h Volatility analysis (High, Low, and Percentage range).
            - Historical performance (ATH and ATL dates/prices).
            - Comparative price change analysis (1h, 24h, 7d, 30d, 60d, 1y).
            - Resource links (GitHub, Whitepaper, and Description).
            Returns None if an API error occurs or data is missing
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

        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None


    def get_market_sentiment(self) -> Optional[str]:
        """
        Analyzes current market psychology and sentiment.

        Returns:
            A formatted string including:
            - Community sentiment (Bullish vs. Bearish percentages).
            - 7-day Fear & Greed Index history (Values and Classifications).
            Returns None if API data from Alternative.me or CoinGecko is missing.
        """
        try:
            alternative_data: dict = self.alternative.get_fear_greed_index()
            coingecko_data: dict = self.coingecko.get_btc_market_data()
            if not alternative_data | coingecko_data:
                return None

            infos: DataBitcoinMarketSentiment = DataBitcoinMarketSentiment.from_data(alternative_data, coingecko_data)

            # Définit : fg_data_1, 2, 3... = [valeur de l'indice fg du jour, classification de cet index]
            fg_lines: list = []

            for i in range(7):
                day_data = infos.fg_data[i]
                if isinstance(day_data, dict):
                    value = day_data.get("value", "N/A")
                    classification = day_data.get("value_classification", "Inconnu")
                else:
                    value = "N/A"
                    classification = "Inconnu"
                fg_lines.append(f"  J+{i}: {value} - {classification}")
            fg_history_txt = "\n".join(fg_lines)

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


        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None


    def get_trending_coins(self) -> Optional[str]:
        """
        Retrieves the list of currently trending cryptocurrencies.

        Returns:
            A Markdown formatted string including:
            - Coin names and symbols.
            - Trending and Market Cap rankings.
            - Current price, 24h historical price, and percentage change.
            - Market Cap and 24h trading volume.
            - A brief description of each trending coin.
            Returns None if an API error occurs or data is empty.
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


        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None

    def get_trending_categories(self) -> Optional[str]:
        """
        Retrieves the list of currently trending cryptocurrency categories.

        Returns:
            A Markdown formatted string including:
            - Category names and rankings.
            - Number of coins within each category.
            - Market Cap and 24h market cap change (current vs. 24h ago).
            - 24h trading volume for the entire category.
            Returns None if an API error occurs or data is empty.
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


        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None

    def get_trending_nfts(self) -> Optional[str]:
        """
        Retrieves the list of currently trending NFT collections.

        Returns:
            A Markdown formatted string including:
            - Collection name and symbol.
            - Floor price and 24h percentage change.
            - 24h trading volume and average sale price.
            - Native currency used for the collection.
            Returns None if an API error occurs or data is empty.
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
                    f"Floor Price: {infos.floor_prices[i]} | 24h Change: {infos.floor_prices_24h_percentage_change[i]}%\n"
                    f"24h Volume: {infos.h24_volumes[i]}\n"
                    f"24h Avg Sale: {infos.h24_avg_sell_price[i]}\n"
                )

            return "\n".join(result)


        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            return None


# Singleton instance for the analyzer
_market_analyser_instance = None

def get_market_analyser_client() -> MarketAnalyzer:
    """Get or create the Cryptocurrency Market Analyzer client singleton instance."""
    global _market_analyser_instance
    if _market_analyser_instance is None:
        _market_analyser_instance = MarketAnalyzer()
    return _market_analyser_instance