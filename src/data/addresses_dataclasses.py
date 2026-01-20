from dataclasses import dataclass

@dataclass
class InfosAddress:
    data: dict

    def __post_init__(self):
        self.chain_stats: dict = self.data.get('chain_stats', {})
        self.mempool_stats: dict = self.data.get('mempool_stats', {})

    @classmethod
    def from_data(cls, data: dict) -> 'InfosAddress':
        return cls(
            data=data
        )


@dataclass
class OverviewAddress:
    data: dict

    def __post_init__(self):
        self.final_balance: float = self.data.get('final_balance',0)
        self.total_received: float = self.data.get('total_received',0)
        self.total_sent: float = self.data.get('total_sent',0)
        self.n_tx: int = self.data.get('n_tx',0)
        self.txs: list = self.data.get('txs',[])

    @classmethod
    def from_data(cls, data: dict) -> 'OverviewAddress':
        return cls(
            data=data
        )
