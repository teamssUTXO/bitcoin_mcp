from typing import Optional

from mcp.server.fastmcp import FastMCP

from src.core.market import get_market_analyser_client


def get_cryptomarket_overview() -> Optional[str]:
    """
    Use this to get cryptomarket overview
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_global_cryptomarket_data()
    return data


def get_bitcoin_price_usd() -> Optional[str]:
    """
    Use this to get bitcoin price usd and others little information
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_btc_price_usd()
    return data


def get_bitcoin_market_data() -> Optional[str]:
    """
    Use this to get bitcoin market data (big report)
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_btc_market_data()
    return data


def get_trending_coins() -> Optional[str]:
    """
    Use this to get top 15 trending coins (sorted by the most popular user searches)
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_trending_coins()
    return data


def get_trending_categories() -> Optional[str]:
    """
    Use this to get top 6 trending categories (sorted by the most popular user searches)
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_trending_categories()
    return data


def get_trending_nfts() -> Optional[str]:
    """
    Use this to get top 7 trending NFTs (sorted by the most popular user searches)
    """

    market_analyzer = get_market_analyser_client()

    data: str = market_analyzer.get_trending_nfts()
    return data

def register_market_tools(mcp: FastMCP):
    """Enregistre tous les tools marché Bitcoin"""
    mcp.add_tool(get_bitcoin_price_usd)
    mcp.add_tool(get_bitcoin_market_data)
    mcp.add_tool(get_cryptomarket_overview)
    mcp.add_tool(get_trending_coins)
    mcp.add_tool(get_trending_categories)
    mcp.add_tool(get_trending_nfts)





