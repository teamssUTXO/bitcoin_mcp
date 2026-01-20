from dataclasses import dataclass
from typing import Optional

@dataclass
class RankingMiningPools:
    data: dict

    def __post_init__(self):
        self.pools: list = self.data.get("pools", [])
        self.top10_pools: list = self.data.get("pools", [])[:10]

    @classmethod
    def from_data(cls, data: dict) -> RankingMiningPools:
        return cls(
            data = data,
        )


@dataclass
class HashratesMiningPools:
    data: dict

    def __post_init__(self):
        self.pools: list = self.data.get("pools", [])[:10]

    @classmethod
    def from_data(cls, data: dict) -> HashratesMiningPools:
        return cls(
            data = data
        )


@dataclass
class TopMiningPool:
    data: dict

    def __post_init__(self):
        self.pools: list = self.data.get("pools", [])


    @classmethod
    def from_data(cls, data: dict) -> TopMiningPool:
        return cls(
            data = data
        )

@dataclass
class MiningPoolBySlug:
    data: dict

    def __post_init__(self):
        self.pool_infos = self.data.get("pool", {})
        self.block_count = self.data.get('blockCount', {})
        self.block_share = self.data.get('blockShare', {})
        self.hashrate = self.data.get("reportedHashrate") or self.data.get("estimatedHashrate", 0)
        self.block_health = self.data.get('avgBlockHealth', 0)
        self.total_reward = self.data.get("totalReward", 0)

        self.name = self.pool_infos.get('name', 'Unknown')
        self.link = self.pool_infos.get('link', "")
        self.addresses = self.pool_infos.get('addresses', [])

    @classmethod
    def from_data(cls, data: dict) -> MiningPoolBySlug:
        return cls(
            data = data
        )