from dataclasses import dataclass


@dataclass
class DataTransactionInfo:
    data: dict

    def __post_init__(self):
        self.vin: list = self.data.get("vin", [])
        self.vout: list = self.data.get("vout", [])
        self.size: int = self.data.get("size", 0)
        self.fee: int = self.data.get("fee", 0)
        self.status: dict = self.data.get("status", {})

    @classmethod
    def from_data(cls, data: dict) -> DataTransactionInfo:
        return cls(
            data=data
        )


@dataclass
class DataTxInput:
    data: dict

    def __post_init__(self):
        self.prev = self.data.get("prevout", {})

        self.txid: str = self.data.get("txid", "")
        self.vout_index: int = self.data.get("vout_index", 0)
        self.address: str = self.prev.get("scriptpubkey_address", "")
        self.value: int = self.prev.get("value", 0)

    @classmethod
    def from_data(cls, data: dict) -> TxInput:
        return cls(
            data=data
        )


@dataclass
class DataTxOutput:
    data: dict

    def __post_init__(self):
        self.address: str = self.data.get('scriptpubkey_address',"")
        self.value: int = self.data.get('value',0)

    @classmethod
    def from_data(cls, data: dict) -> TxOutput:
        return cls(
            data=data
        )


@dataclass
class DataTxInOut:
    data: dict

    def __post_init__(self):
        self.vin: list = self.data.get('vin')
        self.vout: list = self.data.get('vout')


    @classmethod
    def from_data(cls, data: dict) -> TxInOut:
        return cls(
            data=data
        )


@dataclass
class DataTransactionsAddress:
    data: dict

    def __post_init__(self):
        self.txs: list = self.data.get("txs", [])

    @classmethod
    def from_data(cls, data: dict) -> DataTransactionsAddress:
        return cls(
            data=data,
        )
