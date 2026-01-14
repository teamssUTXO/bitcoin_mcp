from dataclasses import dataclass

SATOSHI = 100_000_000

@dataclass
class InfosAddress:
    # Infos principales
    chain_stats: dict
    mempool_stats: dict

    def __post_init__(self):
        self.funded_txo_sum = self.chain_stats["funded_txo_sum"]
        self.spent_txo_sum = self.chain_stats['spent_txo_sum']

        self.balance_btc = (self.funded_txo_sum - self.spent_txo_sum) / SATOSHI

        self.tx_count = self.chain_stats['tx_count']
        self.funded_txo_count = self.chain_stats['funded_txo_count']
        self.spent_txo_count = self.chain_stats['spent_txo_count']

        self.mempool_balance = self.mempool_stats['funded_txo_sum'] - self.mempool_stats['spent_txo_sum']
        self.mempool_tx_count = self.mempool_stats['tx_count']

        if self.balance_btc == 0 and self.tx_count > 0:
            self.category = "Adresse vidée"
        elif self.balance_btc > 1:  # > 1 BTC
            self.category = "Grande balance (> 1 BTC)"
        elif self.balance_btc > 0.1:  # > 0.1 BTC
            self.category = "Balance moyenne"
        elif self.balance_btc > 0:
            self.category = "Petite balance (< 0.1 BTC)"
        else:
            self.category = "Adresse vide"

        if self.mempool_tx_count > 0:
            self.status = "ACTIVE - Transactions en cours"
        elif self.balance_btc > 0:
            self.status = "DORMANTE - Balance existante, aucune TX récente"
        else:
            self.status = "INACTIVE - Balance nulle"

    @classmethod
    def from_data(cls, data: dict) -> 'InfosAddress':
        return cls(
            chain_stats=data.get('chain_stats', {}),
            mempool_stats=data.get('mempool_stats', {}),
        )


@dataclass
class OverviewAddress:
    final_balance: float
    total_received: float
    total_sent: float
    n_tx: int
    # txs: list = field(default_factory=list)

    def __post_init__(self):
        self.balance_btc = self.final_balance / SATOSHI
        self.received_btc = self.total_received / SATOSHI
        self.sent_btc = self.total_sent / SATOSHI
        # self.txs = [
        #     {
        #         "hash": tx.get("hash"),
        #         "time": tx.get("time"),
        #         "result": tx.get("result", 0),
        #         "fee": tx.get("fee", 0),
        #     }
        #     for tx in self.txs
        # ]

    @classmethod
    def from_data(cls, data: dict) -> 'OverviewAddress':
        return cls(
            final_balance = data.get('final_balance',0),
            total_received = data.get('total_received',0),
            total_sent = data.get('total_sent',0),
            n_tx = data.get('n_tx',0),
            # txs = data.get('txs',{}),
        )
