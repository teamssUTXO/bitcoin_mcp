from dataclasses import dataclass
from typing import Optional

@dataclass
class RankingMiningPools:
    pools: list

    def __post_init__(self):
        self.total_blocks = sum(p.get("blockCount", 0) for p in self.pools)

    @classmethod
    def from_data(cls, data: dict) -> RankingMiningPools:
        return cls(
            pools = data.get("pools", [])[:10], # TODO : ça fonctionne ce slicing ? regarde s=pour moi stp
        )



@dataclass
class HashratesMiningPools:
    pools: list

    def __post_init__(self):
        self.total_pools = len(self.pools)

    @classmethod
    def from_data(cls, data: dict) -> HashratesMiningPools:
        return cls(
            pools = data.get("pools", [])[:10], # TODO : ça fonctionne ce slicing ? regarde s=pour moi stp
        )


@dataclass
class TopMiningPool:
    pools: list

    def __post_init__(self):
        self.pool = self.pools[0]

        self.name = self.pool.get('name', 'Unknown')
        self.slug = self.pool.get('slug', 'Unknown')
        self.block_count = self.pool.get('blockCount', 0)
        self.link = self.pool.get('link', "")

        self.total_blocks = sum(p.get('blockCount', 0) for p in self.pools)
        self.percentage = (self.block_count / self.total_blocks * 100) if self.total_blocks > 0 else 0

    @classmethod
    def from_data(cls, data: dict) -> TopMiningPool:
        return cls(
            pools = data.get("pools", [])
        )

@dataclass
class MiningPoolBySlug:
    pool: dict

    def __post_init__(self):
        self.pool_infos = self.pool.get("pool", {})
        self.block_count = self.pool.get('blockCount', {})
        self.block_share = self.pool.get('blockShare', {})
        self.hashrate = self.pool.get("reportedHashrate") or self.pool.get("estimatedHashrate", 0)
        self.block_health = self.pool.get('avgBlockHealth', 0)
        self.total_reward = self.pool.get("totalReward", 0)

        self.name = self.pool_infos.get('name', 'Unknown')
        self.link = self.pool.get('link', "")
        self.addresses = self.pool_infos.get('addresses', [])

    @classmethod
    def from_data(cls, data: dict) -> MiningPoolBySlug:
        return cls(
            pool = data
        )