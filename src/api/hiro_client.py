# from typing import Optional
# from src.api.client import APIClient
# from src.config import Config
#
# class HiroClient(APIClient):
#     def __init__(self):
#         super().__init__(Config.HIRO_API_URL)
#
#     """
#     Renvoie le solde bitcoin d'une adresse
#     Docs : https://docs.hiro.so/en/apis/stacks-blockchain-api/reference/accounts/balances
#     """
#     def get_address_balance(self, address) -> Optional[dict]:
#         return self.get(f"extended/v1/account/{address}/balances", ttl=30)
#
#
#     """
#     Renvoie le solde bitcoin d'une adresse
#     Docs : https://docs.hiro.so/en/apis/stacks-blockchain-api/reference/accounts/transactions
#     """
#     def get_address_transactions(self, address) -> Optional[dict]:
#         return self.get(f"extended/v1/account/{address}/transactions", ttl=30)
#
#
#     """
#     Renvoie le temps moyen de minage des blocs
#     Docs : https://docs.hiro.so/en/apis/stacks-blockchain-api/reference/blocks/
#     """
#     def get_address_blocks(self) -> Optional[dict]:
#         return self.get(f"extended/v2/blocks/average-times", ttl=30)
#
#
#     """
#     Renvoie les ordinals d'une adresse bitcoin
#     Docs : https://docs.hiro.so/en/apis/ordinals-api/reference/inscriptions/get-inscriptions
#     """
#     def get_address_ordinals_inscription(self, address) -> Optional[dict]:
#         return self.get(f"ordinals/v1/inscriptions?address={address}&limit=5", ttl=30)
#
#
#     def get_address_runes_inscription(self, address) -> Optional[dict]:
#         pass