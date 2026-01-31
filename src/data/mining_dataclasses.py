from __future__ import annotations
from dataclasses import dataclass

@dataclass
class DataRankingMiningPools:
    data: dict

    def __post_init__(self):
        self.pools: list = self.data.get("pools", [])
        self.top10_pools: list = self.data.get("pools", [])[:10]

    @classmethod
    def from_data(cls, data: dict) -> DataRankingMiningPools:
        return cls(
            data = data,
        )


@dataclass
class DataHashratesMiningPools:
    data: list

    def __post_init__(self):
        self.pools: list = self.data[:10]

    @classmethod
    def from_data(cls, data: list) -> DataHashratesMiningPools:
        return cls(
            data = data
        )


@dataclass
class DataTopMiningPool:
    data: dict

    def __post_init__(self):
        self.pools: list = self.data.get("pools", [])

    @classmethod
    def from_data(cls, data: dict) -> DataTopMiningPool:
        return cls(
            data = data
        )


@dataclass
class DataMiningPoolBySlug:
    data: dict

    def __post_init__(self):
        self.pool_infos: dict = self.data.get("pool", {})
        self.block_count: int = self.data.get('blockCount', {}).get("all", 0)
        self.block_share: int = self.data.get('blockShare', {}).get("all", 0)
        self.hashrate: int = self.data.get("reportedHashrate") or self.data.get("estimatedHashrate", 0)

        self.name: str = self.pool_infos.get('name', 'Unknown')
        self.link: str = self.pool_infos.get('link', "")
        self.addresses: list = self.pool_infos.get('addresses', [])

    @classmethod
    def from_data(cls, data: dict) -> DataMiningPoolBySlug:
        return cls(
            data = data
        )
