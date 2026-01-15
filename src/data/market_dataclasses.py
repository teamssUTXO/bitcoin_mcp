from dataclasses import dataclass

@dataclass
class MarketOverview:
    # Infos principales
    data: dict

    def __post_init__(self):
        self.active_cryptocurrencies : int = self.data["active_cryptocurrencies"]
        self.upcoming_icos : int = self.data["upcoming_icos"]
        self.ongoing_icos : int = self.data["ongoing_icos"]
        self.ended_icos : int = self.data["ended_icos"]
        self.nb_markets : int = self.data["markets"]
        self.market_cap_change_percentage: float = self.data["market_cap_change_percentage"]

        self.five_biggest_market_cap : dict = self.top5(self.data["total_market_cap"])
        self.five_biggest_market_volume : dict = self.top5(self.data["total_volume"])
        self.five_biggest_market_cap_percentage : dict = dict(list(self.data["market_cap_percentage"].items())[:5])

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
    # Infos principales
    bitcoin: dict

    def __post_init__(self):
        self.usd : float = self.bitcoin["usd"]
        self.usd_market_cap : float = self.bitcoin["usd_market_cap"]
        self.usd_24h_vol : float = self.bitcoin["usd_24h_vol"]
        self.usd_24h_change : float = self.bitcoin["usd_24h_change"]

    @classmethod
    def from_data(cls, data: dict) -> 'BitcoinOverview':
        return cls(
            bitcoin = data
        )


@dataclass
class BitcoinMarket:
    block_time_in_minutes: int
    hashing_algorithm: str
    description: str
    white_paper_link: str
    repo_github_link: str
    genesis_date: str
    market_cap: int
    market_cap_rank: int
    current_price: float
    ath_price: float
    ath_change_percentage: float
    ath_date: str
    atl_price: float
    atl_change_percentage: float
    atl_date: str
    high_price_24h: float
    low_price_24h: float
    total_supply: float
    max_supply: int
    price_change_percentage_1h: float
    price_change_percentage_24h: float
    price_change_percentage_7d: float
    price_change_percentage_14d: float
    price_change_percentage_30d: float
    price_change_percentage_60d: float
    price_change_percentage_200d: float
    price_change_percentage_1y: float

    def __post_init__(self):
        price_1h_before = self.price_before(self.current_price, self.price_change_percentage_1h)
        price_24h_before = self.price_before(self.current_price, self.price_change_percentage_24h)
        price_7d_before = self.price_before(self.current_price, self.price_change_percentage_7d)
        price_14d_before = self.price_before(self.current_price, self.price_change_percentage_14d)
        price_30d_before = self.price_before(self.current_price, self.price_change_percentage_30d)
        price_60d_before = self.price_before(self.current_price, self.price_change_percentage_60d)
        price_200d_before = self.price_before(self.current_price, self.price_change_percentage_200d)
        price_1y_before = self.price_before(self.current_price, self.price_change_percentage_1y)

    @classmethod
    def from_data(cls, data: dict) -> 'BitcoinMarket':
        return cls(
            block_time_in_minutes = data.get("block_time_in_minutes", 0),
            hashing_algorithm = data.get("hashing_algorithm", ""),
            description = data.get("description", ""),
            white_paper_link = data["links"].get("whitepaper", ""),
            repo_github_link = data["links"]["repos_url"]["github"][1],
            genesis_date = data.get("genesis_date", ""),
            market_cap = data["market_data"]["market_cap"].get("usd", 0),
            market_cap_rank = data.get("market_cap_rank", 0),
            current_price = data["market_data"]["current_price"].get("usd", 0),
            ath_price = data["market_data"]["ath"].get("usd", 0),
            ath_change_percentage = data["market_data"]["ath_change_percentage"].get("usd", 0),
            ath_date = data["market_data"]["ath_date"].get("usd", 0),
            atl_price = data["market_data"]["atl"].get("usd", 0),
            atl_change_percentage = data["market_data"]["atl_change_percentage"].get("usd", 0),
            atl_date = data["market_data"]["atl_date"].get("usd", 0),
            high_price_24h = data["market_price"].get("high_24h", 0),
            low_price_24h = data["market_price"].get("low_24h", 0),
            total_supply = data["market_data"].get("total_supply", 0),
            max_supply = data["market_data"].get("max_supply", 0),
            price_change_percentage_1h = data["market_data"]["price_change_percentage_1h_in_currency"].get("usd", 0),
            price_change_percentage_24h = data["market_data"]["price_change_percentage_24h_in_currency"].get("usd", 0),
            price_change_percentage_7d = data["market_data"]["price_change_percentage_7d_in_currency"].get("usd", 0),
            price_change_percentage_14d = data["market_data"]["price_change_percentage_14d_in_currency"].get("usd", 0),
            price_change_percentage_30d = data["market_data"]["price_change_percentage_30d_in_currency"].get("usd", 0),
            price_change_percentage_60d = data["market_data"]["price_change_percentage_60d_in_currency"].get("usd", 0),
            price_change_percentage_200d = data["market_data"]["price_change_percentage_200d_in_currency"].get("usd", 0),
            price_change_percentage_1y = data["market_data"]["price_change_percentage_1y_in_currency"].get("usd", 0),
        )

    @staticmethod
    def price_before(current_price: float, pct_change: float) -> float:
        return current_price / (1 + pct_change / 100)
