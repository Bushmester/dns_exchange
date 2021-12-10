from typing import Any
from uuid import UUID

from bson import ObjectId

from dns_exchange.models.interfaces.users import UserAssetsInterface, UserInterface
from dns_exchange.database import db


class UserAssets(UserAssetsInterface):
    @staticmethod
    def _set_value_by_user_id(user_id: ObjectId, value: Any):
        db[User.table_name].update_one({'id': user_id}, {'$set': {f'{UserAssets.field_name}': set(value)}})

    @staticmethod
    def _get_value_by_user_id(user_id: ObjectId):
        return db[User.table_name].find_one({'id': user_id})


class User(UserInterface):
    @staticmethod
    def _get_assets_descriptor_obj():
        return UserAssets()

    @staticmethod
    def _create_obj(**kwargs):
        db[User.table_name].insert_one({key: val for key, val in kwargs.items()})

    @staticmethod
    def _retrieve_obj(**kwargs):
        return db[User.table_name].find_one({key: val for key, val in kwargs.items()})

    @staticmethod
    def _list_obj(**kwargs):
        return list(db[User.table_name].find({key: val for key, val in kwargs.items()}))

    @staticmethod
    def _update_by_id(obj_id: ObjectId, field_name: str, value: Any):
        db[User.table_name].update_one({'id': obj_id}, {'$set': {field_name: value}})

    @staticmethod
    def _delete_by_id(obj_id: ObjectId):
        db[User.table_name].delete_one({'id': obj_id})
