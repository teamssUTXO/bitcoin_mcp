# # TODO : faire une sécurité ou si pas de api key, on arrete la requete pour dire "pas de clé trouvées, soit en prendre une ici : site ou alors pas possible
#
# import os
# from dotenv import load_dotenv
# from typing import Any, Dict, List, Optional
# from src.api.client import APIClient
# from src.config import Config
#
# load_dotenv()
#
#
# class ElfaClient(APIClient):
#     def __init__(self):
#         super().__init__(Config.ELFA_API_URL, api_key=os.getenv("ELFA_API_KEY"))
#
#     """
#     Renvoie le top 5 des trending coins sur 24h, 7d, 30d
#     Docs : https://mempool.space/docs/api/rest#get-block-tip-height
#     """
#     def get_top_5_trending_coin_1h(self) -> Optional[dict]:
#
#         return self.get("v2/aggregations/trending-tokens?timeWindow=24h", ttl=10)
#
#     """
#         Renvoie le top 5 des trending coins sur 24h, 7d, 30d
#         Docs : https://mempool.space/docs/api/rest#get-block-tip-height
#         """
#
#     def get_top_5_trending_coin_7d(self) -> Optional[dict]:
#         return self.get("v2/aggregations/trending-tokens?timeWindow=7d", ttl=10)
#
#     """
#         Renvoie le top 5 des trending coins sur 24h, 7d, 30d
#         Docs : https://mempool.space/docs/api/rest#get-block-tip-height
#         """
#
#     def get_top_5_trending_coin_30d(self) -> Optional[dict]:
#         return self.get("v2/aggregations/trending-tokens?timeWindow=30d", ttl=10)