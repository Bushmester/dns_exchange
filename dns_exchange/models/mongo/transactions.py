from typing import Any

from bson import ObjectId

from dns_exchange.database import db
from dns_exchange.models.interfaces.transactions import TransactionsInterface


class Transactions(TransactionsInterface):
    @staticmethod
    def _create_obj(**kwargs):
        db[Transactions.table_name].insert_one({key: val for key, val in kwargs.items()})

    @staticmethod
    def _retrieve_obj(**kwargs):
        return db[Transactions.table_name].find_one({key: val for key, val in kwargs.items()})

    @staticmethod
    def _list_obj(**kwargs):
        return list(db[Transactions.table_name].find({key: val for key, val in kwargs.items()}))

    @staticmethod
    def _update_by_id(obj_id: ObjectId, field_name: str, value: Any):
        db[Transactions.table_name].update_one({'id': obj_id}, {'$set': {field_name: value}})

    @staticmethod
    def _delete_by_id(obj_id: ObjectId):
        db[Transactions.table_name].delete_one({'id': obj_id})
