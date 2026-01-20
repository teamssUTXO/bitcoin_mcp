from dataclasses import dataclass

@dataclass
class MarketOverview:
    data: dict

    def __post_init__(self):
        self.active_cryptocurrencies : int = self.data.get("active_cryptocurrencies", 0)
        self.upcoming_icos : int = self.data.get("upcoming_icos", 0)
        self.ongoing_icos : int = self.data.get("ongoing_icos", 0)
        self.ended_icos : int = self.data.get("ended_icos", 0)
        self.nb_markets : int = self.data.get("markets", 0)
        self.market_cap_change_percentage: float = self.data.get("market_cap_change_percentage", 0)

        self.five_biggest_market_cap : dict = self.top5(self.data.get("total_market_cap", {}))
        self.five_biggest_market_volume : dict = self.top5(self.data.get("total_volume", {}))
        self.five_biggest_market_cap_percentage : dict = dict(list(self.data.get("market_cap_percentage", {}).items())[:5])

    @classmethod
    def from_data(cls, data: dict) -> 'MarketOverview':
        return cls(
            data = data
        )

    @staticmethod
    def top5(data: dict) -> dict:
        return dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:5])


@dataclass
class BitcoinOverview:
    data: dict

    def __post_init__(self):
        self.usd : float = self.data.get("usd", 0)
        self.usd_market_cap : float = self.data.get("usd_market_cap", 0)
        self.usd_24h_vol : float = self.data.get("usd_24h_vol", 0)
        self.usd_24h_change : float = self.data.get("usd_24h_change", 0)

    @classmethod
    def from_data(cls, data: dict) -> 'BitcoinOverview':
        return cls(
            data = data
        )


@dataclass
class BitcoinMarket:
    data: dict

    def __post_init__(self):
        self.block_time_in_minutes = self.data.get("block_time_in_minutes", 0)
        self.hashing_algorithm = self.data.get("hashing_algorithm", "")
        self.description = self.data.get("description", "")
        self.white_paper_link = self.data.get("links", {}).get("whitepaper", "")
        self.repo_github_link = self.data.get("links", {}).get("repos_url", {}).get("github", [])[0]
        self.genesis_date = self.data.get("genesis_date", "")
        self.market_cap = self.data.get("market_data", {}).get("market_cap", {}).get("usd", 0)
        self.market_cap_rank = self.data.get("market_cap_rank", 0)
        self.current_price = self.data.get("market_data", {}).get("current_price", {}).get("usd", 0)

        self.ath_price = self.data.get("market_data", {}).get("ath", {}).get("usd", 0)
        self.ath_change_percentage = self.data.get("market_data", {}).get("ath_change_percentage", {}).get("usd", 0)
        self.ath_date = self.data.get("market_data", {}).get("ath_date", {}).get("usd", 0)

        self.atl_price = self.data.get("market_data", {}).get("atl", {}).get("usd", 0)
        self.atl_change_percentage = self.data.get("market_data", {}).get("atl_change_percentage", {}).get("usd", 0)
        self.atl_date = self.data.get("market_data", {}).get("atl_date", {}).get("usd", 0)

        self.high_price_24h = self.data.get("market_price", {}).get("high_24h", 0)
        self.low_price_24h = self.data.get("market_price", {}).get("low_24h", 0)

        self.total_supply = self.data.get("market_data", {}).get("total_supply", 0)
        self.max_supply = self.data.get("market_data", {}).get("max_supply", 0)

        self.price_change_percentage_1h = self.data.get("market_data", {}).get("price_change_percentage_1h_in_currency",{}).get("usd", 0)
        self.price_change_percentage_24h = self.data.get("market_data", {}).get("price_change_percentage_24h_in_currency", {}).get("usd", 0)
        self.price_change_percentage_7d = self.data.get("market_data", {}).get("price_change_percentage_7d_in_currency", {}).get("usd", 0)
        self.price_change_percentage_14d = self.data.get("market_data", {}).get("price_change_percentage_14d_in_currency", {}).get("usd", 0)
        self.price_change_percentage_30d = self.data.get("market_data", {}).get("price_change_percentage_30d_in_currency", {}).get("usd", 0)
        self.price_change_percentage_60d = self.data.get("market_data", {}).get("price_change_percentage_60d_in_currency", {}).get("usd", 0)
        self.price_change_percentage_200d = self.data.get("market_data", {}).get("price_change_percentage_200d_in_currency", {}).get("usd", 0)
        self.price_change_percentage_1y = self.data.get("market_data", {}).get("price_change_percentage_1y_in_currency", {}).get("usd", 0)


        self.price_1h_before = self.price_before(self.current_price, self.price_change_percentage_1h)
        self.price_24h_before = self.price_before(self.current_price, self.price_change_percentage_24h)
        self.price_7d_before = self.price_before(self.current_price, self.price_change_percentage_7d)
        self.price_14d_before = self.price_before(self.current_price, self.price_change_percentage_14d)
        self.price_30d_before = self.price_before(self.current_price, self.price_change_percentage_30d)
        self.price_60d_before = self.price_before(self.current_price, self.price_change_percentage_60d)
        self.price_200d_before = self.price_before(self.current_price, self.price_change_percentage_200d)
        self.price_1y_before = self.price_before(self.current_price, self.price_change_percentage_1y)

    @classmethod
    def from_data(cls, data: dict) -> 'BitcoinMarket':
        return cls(
            data=data,
        )

    @staticmethod
    def price_before(current_price: float, pct_change: float) -> float:
        return current_price / (1 + pct_change / 100)

@dataclass
class BitcoinMarketSentiment:
    alternative_data: dict
    coingecko_data: dict

    def __post_init__(self):
        self.fg_data: list = self.alternative_data.get("data", [])
        self.sentiment_votes_up_percentage: float = self.coingecko_data.get("sentiment_votes_up_percentage", 0)
        self.sentiment_votes_down_percentage: float = self.coingecko_data.get("sentiment_votes_down_percentage", 0)

    @classmethod
    def from_data(cls, alternative_data: dict, coingecko_data: dict) -> 'BitcoinMarketSentiment':
        return cls(
            alternative_data=alternative_data,
            coingecko_data=coingecko_data
        )
