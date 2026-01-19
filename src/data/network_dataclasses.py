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
    fees: dict

    def __post_init__(self):
        self.fastest = self.fees.get("fastestFee", 0)
        self.half_hour = self.fees.get("halfHourFee", 0)
        self.hour = self.fees.get("hourFee", 0)
        self.economy = self.fees.get("economyFee", 0)
        self.minimum = self.fees.get("minimumFee", 0)

    @classmethod
    def from_data(cls, data: dict) -> NetworkFees:
        return cls(
            fees = data
        )


@dataclass
class NetworkHashrate:
    hashrate: int

    def __post_init__(self):
        self.hashrate_eh = self.hashrate / 1_000_000_000_000_000_000

    @classmethod
    def from_data(cls, data: int) -> NetworkHashrate:
        return cls(
            hashrate = data
        )


@dataclass
class NetworkDifficulty:
    difficulty: int

    def __post_init__(self):
        self.difficulty_T = self.difficulty / 1e12

    @classmethod
    def from_data(cls, data: int) -> NetworkDifficulty:
        return cls(
            difficulty = data
        )


@dataclass
class NetworkTransactions:
    transactions_24h: int

    @classmethod
    def from_data(cls, data: int) -> NetworkTransactions:
        return cls(
            transactions_24h = data
        )


@dataclass
class NetworkBTCSent:
    BTCSent_24h: int

    @classmethod
    def from_data(cls, data: int) -> NetworkBTCSent:
        return cls(
            BTCSent_24h = data
        )


@dataclass
class NetworkUnconfirmedTX:
    unconfirmed_tx: int

    @classmethod
    def from_data(cls, data: int) -> NetworkUnconfirmedTX:
        return cls(
            unconfirmed_tx = data
        )


# TODO : à voir avec la doc car là actuellement j'ai pas de co
@dataclass
class DecentralizedMining:
    pools: list

    def __post_init__(self):
        self.total_blocks = sum(p.get("blockCount", 0) for p in self.pools)
        self.sorted_pools = sorted(self.pools, key=lambda x: x.get("blockCount", 0), reverse=True)

        self.top3_blocks = sum(p.get("blockCount", 0) for p in self.sorted_pools[:3])
        self.top3_percentage = (self.top3_blocks / self.total_blocks) * 100 if self.total_blocks > 0 else 0

        self.top5_blocks = sum(p.get("blockCount", 0) for p in self.sorted_pools[:5])
        self.top5_percentage = (self.top5_blocks / self.total_blocks) * 100 if self.total_blocks > 0 else 0

    @classmethod
    def from_data(cls, data: dict) -> DecentralizedMining:
        return cls(
            pools = data.get("pools", []),
        )

    @property
    def evaluation(self) -> Optional[str]:
        if self.top3_percentage > 51:
            return "Risque élevé - Top 3 > 51%"
        elif self.top5_percentage > 75:
            return "Risque moyen - Top 5 > 75%"
        else:
            return "Risque faible - Distribution équilibré"
