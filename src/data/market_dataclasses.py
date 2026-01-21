from dataclasses import dataclass

@dataclass
class DataMarketOverview:
    data: dict

    def __post_init__(self):
        self.active_cryptocurrencies : int = self.data.get("active_cryptocurrencies", 0)
        self.upcoming_icos : int = self.data.get("upcoming_icos", 0)
        self.ongoing_icos : int = self.data.get("ongoing_icos", 0)
        self.ended_icos : int = self.data.get("ended_icos", 0)
        self.nb_markets : int = self.data.get("markets", 0)
        self.market_cap_change_percentage: float = self.data.get("market_cap_change_percentage", 0)
        self.market_cap_percentage: dict = self.data.get("market_cap_percentage", {})

    @classmethod
    def from_data(cls, data: dict) -> DataMarketOverview:
        return cls(
            data = data.get("data", {}) # car double wrap des données
        )


@dataclass
class DataBitcoinOverview:
    data: dict

    def __post_init__(self):
        self.usd : int = self.data.get("usd", 0)
        self.usd_market_cap : int = self.data.get("usd_market_cap", 0)
        self.usd_24h_vol : int = self.data.get("usd_24h_vol", 0)
        self.usd_24h_change : int = self.data.get("usd_24h_change", 0)

    @classmethod
    def from_data(cls, data: dict) -> DataBitcoinOverview:
        return cls(
            data = data
        )


@dataclass
class DataBitcoinMarket:
    data: dict

    def __post_init__(self):
        self.block_time_in_minutes: int = self.data.get("block_time_in_minutes", 0)
        self.hashing_algorithm: str = self.data.get("hashing_algorithm", "")
        self.description: str = self.data.get("description", "")
        self.white_paper_link: str = self.data.get("links", {}).get("whitepaper", "")
        self.repo_github_link: str = self.data.get("links", {}).get("repos_url", {}).get("github", [])[0]
        self.genesis_date: str = self.data.get("genesis_date", "")
        self.market_cap: int = self.data.get("market_data", {}).get("market_cap", {}).get("usd", 0)
        self.market_cap_rank: int = self.data.get("market_cap_rank", 0)
        self.current_price: int = self.data.get("market_data", {}).get("current_price", {}).get("usd", 0)

        self.ath_price: int = self.data.get("market_data", {}).get("ath", {}).get("usd", 0)
        self.ath_change_percentage: int = self.data.get("market_data", {}).get("ath_change_percentage", {}).get("usd", 0)
        self.ath_date: int = self.data.get("market_data", {}).get("ath_date", {}).get("usd", 0)

        self.atl_price: int = self.data.get("market_data", {}).get("atl", {}).get("usd", 0)
        self.atl_change_percentage: int = self.data.get("market_data", {}).get("atl_change_percentage", {}).get("usd", 0)
        self.atl_date: int = self.data.get("market_data", {}).get("atl_date", {}).get("usd", 0)

        self.high_price_24h: int = self.data.get("market_price", {}).get("high_24h", 0)
        self.low_price_24h: int = self.data.get("market_price", {}).get("low_24h", 0)

        self.total_supply: int = self.data.get("market_data", {}).get("total_supply", 0)
        self.max_supply: int = self.data.get("market_data", {}).get("max_supply", 0)

        self.price_change_percentage_1h: int = self.data.get("market_data", {}).get("price_change_percentage_1h_in_currency",{}).get("usd", 0)
        self.price_change_percentage_24h: int = self.data.get("market_data", {}).get("price_change_percentage_24h_in_currency", {}).get("usd", 0)
        self.price_change_percentage_7d: int = self.data.get("market_data", {}).get("price_change_percentage_7d_in_currency", {}).get("usd", 0)
        self.price_change_percentage_14d: int = self.data.get("market_data", {}).get("price_change_percentage_14d_in_currency", {}).get("usd", 0)
        self.price_change_percentage_30d: int = self.data.get("market_data", {}).get("price_change_percentage_30d_in_currency", {}).get("usd", 0)
        self.price_change_percentage_60d: int = self.data.get("market_data", {}).get("price_change_percentage_60d_in_currency", {}).get("usd", 0)
        self.price_change_percentage_200d: int = self.data.get("market_data", {}).get("price_change_percentage_200d_in_currency", {}).get("usd", 0)
        self.price_change_percentage_1y: int = self.data.get("market_data", {}).get("price_change_percentage_1y_in_currency", {}).get("usd", 0)

        self.price_1h_before: float = self.price_before(self.current_price, self.price_change_percentage_1h)
        self.price_24h_before: float = self.price_before(self.current_price, self.price_change_percentage_24h)
        self.price_7d_before: float = self.price_before(self.current_price, self.price_change_percentage_7d)
        self.price_14d_before: float = self.price_before(self.current_price, self.price_change_percentage_14d)
        self.price_30d_before: float = self.price_before(self.current_price, self.price_change_percentage_30d)
        self.price_60d_before: float = self.price_before(self.current_price, self.price_change_percentage_60d)
        self.price_200d_before: float = self.price_before(self.current_price, self.price_change_percentage_200d)
        self.price_1y_before: float = self.price_before(self.current_price, self.price_change_percentage_1y)

    @classmethod
    def from_data(cls, data: dict) -> DataBitcoinMarket:
        return cls(
            data=data,
        )

    @staticmethod
    def price_before(current_price: int, pct_change: int) -> float:
        return current_price / (1 + pct_change / 100)


@dataclass
class DataBitcoinMarketSentiment:
    alternative_data: dict
    coingecko_data: dict

    def __post_init__(self):
        self.fg_data: list = self.alternative_data.get("data", [])
        self.sentiment_votes_up_percentage: int = self.coingecko_data.get("sentiment_votes_up_percentage", 0)
        self.sentiment_votes_down_percentage: int = self.coingecko_data.get("sentiment_votes_down_percentage", 0)

    @classmethod
    def from_data(cls, alternative_data: dict, coingecko_data: dict) -> DataBitcoinMarketSentiment:
        return cls(
            alternative_data=alternative_data,
            coingecko_data=coingecko_data
        )


@dataclass
class DataTrendingCoins:
    data: list

    def __post_init__(self):
        self.names: list = [item.get("item", {}).get("name", "") for item in self.data]
        self.symbols: list = [item.get("item", {}).get("symbol", "") for item in self.data]

        self.market_cap_ranks: list = [item.get("item", {}).get("market_cap_rank", "") for item in self.data]

        self.ranks: list = [item.get("item", {}).get("score", "") for item in self.data]

        self.prices: list = [item.get("item", {}).get("data", {}).get("price", 0) for item in self.data]
        self.prices_changed: list = [item.get("item", {}).get("data", {}).get("price_change_percentage_24h", {}).get("usd", 0) for item in self.data]

        self.market_caps: list = [item.get("item", {}).get("data", {}).get("market_cap", 0) for item in self.data]
        self.total_volumes: list = [item.get("item", {}).get("data", {}).get("total_volume", 0) for item in self.data]

        self.descriptions: list = [(item.get("item", {}).get("data", {}).get("content", {}) or {}).get("description", "description unavailable for this coin") for item in self.data]

    @classmethod
    def from_data(cls, data: dict) -> DataTrendingCoins:
        return cls(
            data=data.get("coins", [])  # on découpe en trois la donnée pour coins, categories et nft, plus opti
        )


@dataclass
class DataTrendingCategories:
    data: list

    def __post_init__(self):
        self.names: list = [item.get("name", "") for item in self.data]
        self.n_coins_count: list = [item.get("coins_count", "") for item in self.data]

        self.market_caps: list = [item.get("data", {}).get("market_cap", 0) for item in self.data]
        self.total_volumes: list = [item.get("data", {}).get("total_volume", 0) for item in self.data]

        self.market_caps_changed: list = [item.get("data", {}).get("market_cap_change_percentage_24h", {}).get("usd", 0) for item in self.data]

    @classmethod
    def from_data(cls, data: dict) -> DataTrendingCategories:
        return cls(
            data=data.get("categories", [])  # on découpe en trois la donnée pour coins, categories et nft, plus opti
        )


@dataclass
class DataTrendingNFTs:
    data: list

    def __post_init__(self):
        self.names: list = [item.get("name", "") for item in self.data]
        self.symbols: list = [item.get("symbol", "") for item in self.data]

        self.native_currencies: list = [item.get("native_currency_symbol", ""). upper() for item in self.data]

        self.floor_prices: list = [item.get("data", {}).get("floor_price", "") for item in self.data]
        self.floor_prices_24h_percentage_change: list = [item.get("data", {}).get("floor_price_in_usd_24h_percentage_change") for item in self.data]

        self.h24_volumes: list = [item.get("data", {}).get("h24_volume", "") for item in self.data]
        self.h24_avg_sell_price: list = [item.get("data", {}).get("h24_average_sale_price", "") for item in self.data]

    @classmethod
    def from_data(cls, data: dict) -> DataTrendingNFTs:
        return cls(
            data=data.get("nfts", [])  # on découpe en trois la donnée pour coins, categories et nft, plus opti
        )