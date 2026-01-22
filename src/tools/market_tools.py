from typing import Optional

from mcp.server.fastmcp import FastMCP

from src.core.market import get_market_analyser_client


def get_cryptomarket_overview() -> Optional[str]:
    """
    Use this to get a comprehensive overview of the global cryptocurrency market conditions and metrics.

    Returns detailed metrics in string format:
    - Total number of active cryptocurrencies
    - Total number of trading markets
    - Overall market cap percentage change
    - ICO status breakdown (upcoming, ongoing, ended)
    - Total market capitalization (formatted by currency)
    - Total trading volume (formatted by currency)
    - Top 5 cryptocurrencies by market dominance percentage

    Use cases: When you need a broad view of the entire crypto ecosystem health, to understand market trends, or to see which cryptocurrencies dominate the market.
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_global_cryptomarket_data()
    return data


def get_bitcoin_price_usd() -> Optional[str]:
    """
    Use this to get Bitcoin's current USD price and essential market indicators.

    Returns key metrics in string format:
    - Current Bitcoin price in USD
    - Estimated price 24 hours ago
    - 24-hour price change percentage
    - Total market capitalization in USD
    - 24-hour trading volume in USD
    - Volume-to-Cap ratio (liquidity indicator)
    - Circulating supply (number of tokens)

    Use cases: When you need a quick Bitcoin price check with essential market context.
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_btc_price_usd()
    return data


def get_bitcoin_market_data() -> Optional[str]:
    """
    Use this to get a comprehensive technical and financial report on Bitcoin with extensive historical data and market analysis.

    Returns an extensive report in string format including:

    **Core Metrics:**
    - Current price (USD) and market cap rank
    - Total market capitalization
    - Genesis date (blockchain creation date)

    **Tokenomics & Supply:**
    - Total supply and max supply
    - Fully Diluted Valuation (FDV)
    - Hashing algorithm and block time

    **24-Hour Volatility:**
    - Highest and lowest prices in last 24h
    - Volatility percentage and price gap

    **Historical Performance:**
    - All-Time High (ATH) price, date, and percentage drop from ATH
    - All-Time Low (ATL) price, date, and percentage rise from ATL

    **Multi-Timeframe Price Analysis:**
    - Price changes over 1 hour, 24 hours, 7 days, 30 days, 60 days, and 1 year
    - Previous prices for each timeframe for trend comparison

    **Additional Information:**
    - GitHub repository link
    - Whitepaper link
    - Detailed project description

    Use cases: When you need in-depth Bitcoin market analysis, historical performance tracking, or comprehensive investment research data. For quick price checks, use `get_bitcoin_price_usd`.
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_btc_market_data()
    return data

def get_bitcoin_market_sentiment() -> Optional[str]:
    """
    Use this to get a comprehensive sentiment analysis of the Bitcoin market based on community voting and the Fear & Greed Index.

    Returns detailed psychological metrics in string format:

    **Community Sentiment (CoinGecko):**
    - Overall market trend label (bullish/bearish/neutral)
    - Percentage of optimistic votes (thumbs up)
    - Percentage of pessimistic votes (thumbs down)

    **Fear & Greed Index History (7 days):**
    - Daily Fear & Greed Index values from Alternative.me
    - Historical trend showing market emotion evolution over the past week
    - Index ranges from 0 (Extreme Fear) to 100 (Extreme Greed)

    Use cases: When you need to gauge overall market sentiment, understand investor psychology, or determine if the market is in fear or greed mode.
    """

    market_analyzer = get_market_analyser_client()
    data: str = market_analyzer.get_market_sentiment()
    return data


def get_trending_coins() -> Optional[str]:
    """
    Use this to get the top 15 trending cryptocurrencies sorted by the most popular user searches on CoinGecko.

    Returns detailed metrics in string format for each of the 15 trending coins:
    - Coin name and symbol
    - Trending rank (1-15 based on search popularity)
    - Current price in USD (up to 8 decimal places for precision)
    - Price 24 hours ago with percentage change
    - Market capitalization in USD
    - Market cap rank (global ranking by market size)
    - Total 24-hour trading volume in USD
    - Brief project description

    Use cases: When you need to discover what cryptocurrencies are currently attracting the most attention, identify emerging trends, or find coins gaining popularity.
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_trending_coins()
    return data


def get_trending_categories() -> Optional[str]:
    """
    Use this to get the top 6 trending cryptocurrency categories sorted by the most popular user searches on CoinGecko.

    Returns detailed metrics in string format for each of the 6 trending categories:
    - Category name and trending rank (1-6)
    - Number of coins in the category
    - Total market capitalization in USD for the entire category
    - Market cap 24 hours ago with percentage change
    - Total 24-hour trading volume in USD across all coins in the category

    Categories represent thematic groups of cryptocurrencies (e.g., "DeFi", "Layer 1", "Meme Coins", "NFT", "GameFi", etc.).

    Use cases: When you need to identify which cryptocurrency sectors are gaining attention, understand macro trends in the crypto ecosystem, or find emerging narratives. This is based on real user search behavior for category pages.
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_trending_categories()
    return data


def get_trending_nfts() -> Optional[str]:
    """
    Use this to get the top 7 trending NFT collections sorted by the most popular user searches on CoinGecko.

    Returns detailed metrics in string format for each of the 7 trending NFT collections:
    - NFT collection name and symbol
    - Trending rank (1-7 based on search popularity)
    - Native currency used for trading (e.g., ETH, SOL, MATIC)
    - Current floor price (lowest price to buy one NFT from the collection)
    - Floor price percentage change in the last 24 hours
    - Total trading volume in the last 24 hours
    - Average sale price in the last 24 hours

    Use cases: When you need to discover which NFT collections are currently attracting the most attention, identify trending digital art or collectibles, or monitor NFT market activity. This is based on real user search behavior.
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_trending_nfts()
    return data

def register_market_tools(mcp: FastMCP):
    """Registers all Bitcoin market tools"""
    mcp.add_tool(get_bitcoin_price_usd)
    mcp.add_tool(get_bitcoin_market_data)
    mcp.add_tool(get_cryptomarket_overview)
    mcp.add_tool(get_bitcoin_market_sentiment)
    mcp.add_tool(get_trending_coins)
    mcp.add_tool(get_trending_categories)
    mcp.add_tool(get_trending_nfts)





