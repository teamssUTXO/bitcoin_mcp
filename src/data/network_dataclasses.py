from dataclasses import dataclass


@dataclass
class DataNetworkStats:
    data: dict

    def __post_init__(self):
        self.market_price_usd: int = self.data.get("market_price_usd", 0)
        self.hash_rate: int = self.data.get("hash_rate", 0)
        self.total_fees_btc: int = self.data.get("total_fees_btc", 0)
        self.n_btc_mined: int = self.data.get("n_btc_mined", 0)
        self.n_tx: int = self.data.get("n_tx", 0)
        self.n_blocks_mined: int = self.data.get("n_blocks_mined", 0)
        self.minutes_between_blocks: int = self.data.get("minutes_between_blocks", 0)
        self.totalbc: int = self.data.get("totalbc", 0)
        self.n_blocks_total: int = self.data.get("n_blocks_total", 0)
        self.estimated_transaction_volume_usd: int = self.data.get("estimated_transaction_volume_usd", 0)
        self.blocks_size: int = self.data.get("blocks_size", 0)
        self.miners_revenues_usd: int = self.data.get("miners_revenues_usd", 0)
        self.nextretarget: int = self.data.get("nextretarget", 0)
        self.difficulty: int = self.data.get("difficulty", 0)
        self.estimated_btc_sent: int = self.data.get("estimated_btc_sent", 0)
        self.miners_revenue_btc: int = self.data.get("miners_revenue_btc", 0)
        self.total_btc_sent: int = self.data.get("total_btc_sent", 0)
        self.trade_volume_btc: int = self.data.get("trade_volume_btc", 0)
        self.trade_volume_usd: int = self.data.get("trade_volume_usd", 0)

    @classmethod
    def from_data(cls, data: dict) -> DataNetworkStats:
        return cls(
            data=data
        )


@dataclass
class DataNetworkFees:
    data: dict

    def __post_init__(self):
        self.fastest: int = self.data.get("fastestFee", 0)
        self.half_hour: int = self.data.get("halfHourFee", 0)
        self.hour: int = self.data.get("hourFee", 0)
        self.economy: int = self.data.get("economyFee", 0)
        self.minimum: int = self.data.get("minimumFee", 0)

    @classmethod
    def from_data(cls, data: dict) -> DataNetworkFees:
        return cls(
            data = data
        )
