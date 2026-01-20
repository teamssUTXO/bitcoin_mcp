from dataclasses import dataclass, field
from src.config import Config
from datetime import datetime


@dataclass
class TransactionInfo:
    data: dict

    def __post_init__(self):
        self.vin: list = self.data.get("vin", [])
        self.vout: list = self.data.get("vout", [])
        self.size: int = self.data.get("size", 0)
        self.fee: int = self.data.get("fee", 0)
        self.status: dict = self.data.get("status", {})

    @classmethod
    def from_data(cls, data: dict) -> 'TransactionInfo':
        return cls(
            data=data
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
            txid = data.get('txid',""),
            vout_index = data.get('vout_index',0),
            address = prev.get('scriptpubkey_address',""),
            value = prev.get('value',0)
        )


@dataclass
class TxOutput:
    address: str
    value: int

    @classmethod
    def from_data(cls, data: dict) -> 'TxOutput':
        return cls(
            address = data.get('scriptpubkey_address',""),
            value = data.get('value',0)
        )


@dataclass
class TxInOut:
    data: dict

    def __post_init__(self):
        self.vin: list = self.data.get('vin')
        self.vout: list = self.data.get('vout')


    @classmethod
    def from_data(cls, data: dict) -> 'TxInOut':
        return cls(
            data=data
        )


@dataclass
class TransactionsAddress:
    data: dict

    def __post_init__(self):
        self.txs: list = self.data.get("txs", [])

    @classmethod
    def from_data(cls, data: dict) -> 'TransactionsAddress':
        return cls(
            data=data,
        )


