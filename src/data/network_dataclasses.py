from dataclasses import dataclass
from typing import Optional


@dataclass
class NetworkStats:
    data: dict

    def __post_init__(self):
        self.market_price_usd = self.data.get("market_price_usd", 0)
        self.hash_rate = self.data.get("hash_rate", 0)
        self.total_fees_btc = self.data.get("total_fees_btc", 0)
        self.n_btc_mined = self.data.get("n_btc_mined", 0)
        self.n_tx = self.data.get("n_tx", 0)
        self.n_blocks_mined = self.data.get("n_blocks_mined", 0)
        self.minutes_between_blocks = self.data.get("minutes_between_blocks", 0)
        self.totalbc = self.data.get("totalbc", 0)
        self.n_blocks_total = self.data.get("n_blocks_total", 0)
        self.estimated_transaction_volume_usd = self.data.get("estimated_transaction_volume_usd", 0)
        self.blocks_size = self.data.get("blocks_size", 0)
        self.miners_revenue_usd = self.data.get("miners_revenues_usd", 0)
        self.nextretarget = self.data.get("nextretarget", 0)
        self.difficulty = self.data.get("difficulty", 0)
        self.estimated_btc_sent = self.data.get("estimated_btc_sent", 0)
        self.miners_revenue_btc = self.data.get("miners_revenue_btc", 0)
        self.total_btc_sent = self.data.get("total_btc_sent", 0)
        self.trade_volume_btc = self.data.get("trade_volume_btc", 0)
        self.trade_volume_usd = self.data.get("trade_volume_usd", 0)

    @classmethod
    def from_data(cls, data: dict) -> NetworkStats:
        return cls(
            data=data
        )


@dataclass
class NetworkFees:
    data: dict

    def __post_init__(self):
        self.fastest = self.data.get("fastestFee", 0)
        self.half_hour = self.data.get("halfHourFee", 0)
        self.hour = self.data.get("hourFee", 0)
        self.economy = self.data.get("economyFee", 0)
        self.minimum = self.data.get("minimumFee", 0)

    @classmethod
    def from_data(cls, data: dict) -> NetworkFees:
        return cls(
            data = data
        )
