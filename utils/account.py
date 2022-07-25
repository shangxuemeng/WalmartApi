# coding=utf-8

import orjson
from .log import logger
from .request import request
# from service.walmart import WalmartApi


class AccountError(Exception):

    def __init__(self, account_id):
        self.account_id = account_id

    def __str__(self):
        return f"AccountError: id:{self.account_id}"


class BaseAccount:
    url = "https://pams.bailuntec.com/Api/GetAccountToken"

    @classmethod
    async def get_account(cls, account_id) -> dict:
        try:
            json_data = await request("GET", url=cls.url, params={"id": account_id})
            for account_info in json_data["Data"]:
                if account_info.get("Id") == account_id:
                    return account_info
        except Exception as e:
            logger.error(e, exc_info=e)
        raise AccountError(account_id)


class Account:

    @classmethod
    async def get_account(cls, account_id):
        try:
            account_info = await BaseAccount.get_account(account_id)
            auth_json = orjson.loads(account_info["DeveloperJson"])
            return {
                "client_id": auth_json["ClientId"],
                "client_secret": auth_json["ClientSecret"]
            }
        except AccountError:
            raise
        except Exception as e:
            logger.error(e, exc_info=e)
            raise


# class Token():
#     @classmethod
#     async def get_token(cls, account_id):
#         url = 'https://marketplace.walmartapis.com/v3/token'
#         print()
#         try:
#             json_data = await request("POST", url=url, data={"grant_type": 'client_credentials'})
#             print('xxxx', json_data)
#             if json_data.get("access_token"):
#                 # print('xxxxxx', json_data['access_token'])
#                 return json_data['access_token']
#         except Exception as e:
#             logger.error(e, exc_info=e)
#         raise AccountError(account_id)
