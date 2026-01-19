from dataclasses import dataclass

@dataclass
class LatestBlock:
    block: dict

    def __post_init__(self):
        self.hash = self.block.get("hash", "")
        self.timestamp = self.block.get("time", "")
        self.block_index = self.block.get("block_index", 0)
        self.height = self.block.get("height", 0)

    @classmethod
    def from_data(cls, data: dict) -> LatestBlock:
        return cls(
            block = data
        )


@dataclass()
class LatestsBlocks:
    blocks: list[dict]

    def __post_init__(self):
        self.ids = [block.get("id", 0) for block in self.blocks]
        self.heights = [block.get("height", 0) for block in self.blocks]
        self.timestamps = [block.get("timestamp", 0) for block in self.blocks]
        self.txs_count = [block.get("tx_count", 0) for block in self.blocks]
        self.sizes = [block.get("size", 0) for block in self.blocks]
        self.weights = [block.get("weight", 0) for block in self.blocks]
        self.rewards = [block.get("reward", 0) for block in self.blocks]
        self.totalsFees = [block.get("totalFees", 0) for block in self.blocks]
        self.avgsFeeRate = [block.get("avgFeeRate", 0) for block in self.blocks]
        self.pools_slug = [block["pool"].get("slug", "Unknown") for block in self.blocks]
        self.nonces = [block.get("nonce", 0) for block in self.blocks]


    @classmethod
    def from_data(cls, data: list[dict]) -> LatestsBlocks:

        return cls(
            blocks = data
        )