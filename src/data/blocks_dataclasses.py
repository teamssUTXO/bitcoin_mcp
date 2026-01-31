from __future__ import annotations
from dataclasses import dataclass

@dataclass
class DataLatestBlock:
    data: dict

    def __post_init__(self):
        self.hash: str = self.data.get("hash", "")
        self.timestamp: int = self.data.get("time", 0)
        self.block_index: int = self.data.get("block_index", 0)
        self.height: int = self.data.get("height", 0)

    @classmethod
    def from_data(cls, data: dict) -> DataLatestBlock:
        return cls(
            data = data
        )


@dataclass()
class DataLatestBlocks:
    data: list[dict]

    def __post_init__(self):
        self.ids: list = [block.get("id", "") for block in self.data]
        self.heights: list = [block.get("height", 0) for block in self.data]
        self.timestamps: list = [block.get("timestamp", 0) for block in self.data]
        self.txs_count: list = [block.get("tx_count", 0) for block in self.data]
        self.sizes: list = [block.get("size", 0) for block in self.data]
        self.weights: list = [block.get("weight", 0) for block in self.data]
        self.rewards: list = [block.get("extras", {}).get("reward", 0) for block in self.data]
        self.totalsFees: list = [block.get("extras", {}).get("totalFees", 0) for block in self.data]
        self.avgsFeeRate: list = [block.get("extras", {}).get("avgFeeRate", 0) for block in self.data]
        self.pools_slug: list = [block.get("extras", {}).get("pool", {}).get("slug", "Unknown") for block in self.data]
        self.nonces: list = [block.get("nonce", 0) for block in self.data]

    @classmethod
    def from_data(cls, data: list[dict]) -> DataLatestBlocks:
        return cls(
            data = data
        )
