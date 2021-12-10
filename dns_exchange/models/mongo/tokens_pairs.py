from typing import Any

from bson import ObjectId

from dns_exchange.database import db
from dns_exchange.models.interfaces.tokens_pairs import TokenPairsInterface, TokenBuyOrdersInterface, TokenSellOrdersInterface


class TokenBuyOrders(TokenBuyOrdersInterface):
    @staticmethod
    def _set_value_by_user_id(user_id: ObjectId, value: Any):
        db[TokenPairs.table_name].update_one({'id': user_id}, {'$set': {f'{TokenBuyOrders.field_name}': set(value)}})

    @staticmethod
    def _get_value_by_user_id(user_id: ObjectId):
        return db[TokenPairs.table_name].find_one({'id': user_id})


class TokenSellOrders(TokenSellOrdersInterface):
    @staticmethod
    def _set_value_by_user_id(user_id: ObjectId, value: Any):
        db[TokenPairs.table_name].update_one({'id': user_id}, {'$set': {f'{TokenSellOrders.field_name}': set(value)}})

    @staticmethod
    def _get_value_by_user_id(user_id: ObjectId):
        return db[TokenPairs.table_name].find_one({'id': user_id})


class TokenPairs(TokenPairsInterface):
    @staticmethod
    def _get_buy_orders_descriptor_obj():
        return TokenBuyOrders()

    @staticmethod
    def _get_sell_orders_descriptor_obj():
        return TokenSellOrders()

    @staticmethod
    def _create_obj(**kwargs):
        db[TokenPairs.table_name].insert_one({key: val for key, val in kwargs.items()})

    @staticmethod
    def _retrieve_obj(**kwargs):
        return db[TokenPairs.table_name].find_one({key: val for key, val in kwargs.items()})

    @staticmethod
    def _list_obj(**kwargs):
        return list(db[TokenPairs.table_name].find({key: val for key, val in kwargs.items()}))

    @staticmethod
    def _update_by_id(obj_id: ObjectId, field_name: str, value: Any):
        db[TokenPairs.table_name].update_one({'id': obj_id}, {'$set': {field_name: value}})

    @staticmethod
    def _delete_by_id(obj_id: ObjectId):
        db[TokenPairs.table_name].delete_one({'id': obj_id})
