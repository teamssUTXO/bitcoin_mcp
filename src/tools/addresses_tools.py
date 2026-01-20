from typing import Optional

from mcp.server.fastmcp import FastMCP
from src.core.addresses import get_addresses_analyser_client


def get_info_about_address(address: str) -> Optional[str]:
    """
    Use this to get more information about an address

    Args:
        address: address of the address to analyzer
    """

    if not address:
        return "no parameters"

    addresses_analyzer = get_addresses_analyser_client()

    data: str = addresses_analyzer.get_address_info(address)
    return data


def get_address_overview(address: str) -> Optional[str]:
    """
    Use this to get more overview of an address

    Args:
        address: address to get an overview about it
    """

    if not address:
        return "no parameters"

    addresses_analyzer = get_addresses_analyser_client()

    data: str = addresses_analyzer.get_address_info_overview(address)
    return data


def register_addresses_tools(mcp: FastMCP):
    """Enregistre tous les tools des adresses Bitcoin"""
    mcp.add_tool(get_info_about_address)
    mcp.add_tool(get_address_overview)





