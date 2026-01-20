from dataclasses import dataclass

@dataclass
class LatestBlock:
    data: dict

    def __post_init__(self):
        self.hash = self.data.get("hash", "")
        self.timestamp = self.data.get("time", "")
        self.block_index = self.data.get("block_index", 0)
        self.height = self.data.get("height", 0)

    @classmethod
    def from_data(cls, data: dict) -> LatestBlock:
        return cls(
            data = data
        )


@dataclass()
class LatestBlocks:
    data: list[dict]

    def __post_init__(self):
        self.ids = [block.get("id", 0) for block in self.data]
        self.heights = [block.get("height", 0) for block in self.data]
        self.timestamps = [block.get("timestamp", 0) for block in self.data]
        self.txs_count = [block.get("tx_count", 0) for block in self.data]
        self.sizes = [block.get("size", 0) for block in self.data]
        self.weights = [block.get("weight", 0) for block in self.data]
        self.rewards = [block.get("reward", 0) for block in self.data]
        self.totalsFees = [block.get("totalFees", 0) for block in self.data]
        self.avgsFeeRate = [block.get("avgFeeRate", 0) for block in self.data]
        self.pools_slug = [block["pool"].get("slug", "Unknown") for block in self.data]
        self.nonces = [block.get("nonce", 0) for block in self.data]

    @classmethod
    def from_data(cls, data: list[dict]) -> LatestBlocks:

        return cls(
            data = data
        )
