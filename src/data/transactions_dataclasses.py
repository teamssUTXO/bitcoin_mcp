from dataclasses import dataclass, field
from src.config import Config
from datetime import datetime


@dataclass
class TransactionInfo:
    # Infos principales
    vin: list
    vout: list
    size: int
    fee: int
    status: dict

    inputs: list = field(init=False)
    outputs: list = field(init=False)

    def __post_init__(self):
        self.nb_inputs = len(self.vin)
        self.nb_outputs = len(self.vout)

        self.fee_btc = self.fee / Config.SATOSHI

        self.fee_rate = self.fee_btc /self.size if self.size > 0 else 0

        self.transaction_status = ("COMFIRMED" if self.status.get("confirmed") else "UNCOMFIRMED")
        self.transaction_block_time = self.status.get('block_time', 0)
        self.transaction_block_hash = self.status.get('block_hash', '')
        self.transaction_block_height = self.status.get('block_height', 0)

        self.date_str = datetime.fromtimestamp(self.transaction_block_time).strftime('%Y-%m-%d %H:%M:%S') if self.transaction_block_time else 'Non confirmée'

    @classmethod
    def from_data(cls, data: dict) -> 'TransactionInfo':
        return cls(
            vin=data.get(['vin']),
            vout=data.get(['vout']),
            size=data.get(["size"]),
            fee=data.get(['fee']),
            status=data.get(['status']),

        )


@dataclass
class TxInput:
    txid: str
    vout_index: int
    address: str
    value: int

    @classmethod
    def from_data(cls, data: dict) -> 'TxInput':
        prev = data.get("prevout", {})
        return cls(
            txid = data.get(['txid'],""),
            vout_index = data.get(['vout_index'],0),
            address = prev.get(['scriptpubkey_address'],""),
            value = prev.get(['value'],0)
        )


@dataclass
class TxOutput:
    address: str
    value: int

    @classmethod
    def from_data(cls, data: dict) -> 'TxOutput':
        return cls(
            address = data.get(['scriptpubkey_address'],""),
            value = data.get(['value'],0)
        )


@dataclass
class TxInOut:
    # Infos principales
    vin: list
    vout: list

    inputs: list = field(init=False)
    outputs: list = field(init=False)

    def __post_init__(self):
        self.inputs = [TxInput.from_data(v) for v in self.vin]
        self.outputs = [TxOutput.from_data(v) for v in self.vout]


    @classmethod
    def from_data(cls, data: dict) -> 'TxInOut':
        return cls(
            vin=data.get(['vin']),
            vout=data.get(['vout'])
        )

    @property
    def total_input_sats(self):
        return sum(i.value for i in self.inputs)

    @property
    def total_output_sats(self):
        return sum(o.value for o in self.outputs)

    @property
    def total_input_btc(self):
        return self.total_input_sats / Config.SATOSHI

    @property
    def total_output_btc(self):
        return self.total_output_sats / Config.SATOSHI

    @property
    def change_sats(self):
        return self.total_input_sats - self.total_output_sats - self.fee

    @property
    def addresses_in(self):
        return [i.address for i in self.inputs]

    @property
    def addresses_out(self):
        return [o.address for o in self.outputs]


@dataclass
class TransactionsAddress:
    txs: list

    def __post_init__(self):
        self.len_txs = len(self.txs)

        self.txs_hash = [tx["hash"] for tx in self.txs]
        self.txs_date = [datetime.fromtimestamp(tx["time"]) for tx in self.txs]

        self.amount_sent = [
            sum(
                vin.get("prev_out", {}).get("value", 0)
                for vin in tx.get("inputs", [])
                if vin.get("prev_out", {}).get("addr") == self.address
            )
            for tx in self.txs
        ]

        # Destinations (adresse + montant)
        self.destinations = [
            [
                (o.get("addr", ""), o.get("value", 0))
                for o in tx.get("out", [])
            ]
            for tx in self.txs
        ]

    @classmethod
    def from_data(cls, data: dict) -> 'TransactionsAddress':
        return cls(
            txs=data.get(['txs']),
        )


