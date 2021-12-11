from typing import Any, List

from dns_exchange.models.interfaces.users import UserAssetsInterface, UserInterface
from dns_exchange.database import db


class UserAssets(UserAssetsInterface):
    def _set_value(self, key: str, value: Any):
        db[User.table_name].update_one({'id': self._owner_id.id}, {'$set': {f'{UserAssets.field_name}.{key}': value}})

    def _get_value(self, key: str):
        return db[User.table_name].find_one({'id': self._owner_id.id})[UserAssets.field_name][key]

    def _delete_value(self, key: str):
        db[User.table_name].update_one({'id': self._owner_id.id}, {'$unset': {f'{UserAssets.field_name}.{key}': None}})

    def _list_values(self):
        return db[User.table_name].find_one({'id': self._owner_id.id})[UserAssets.field_name]


class User(UserInterface):
    @staticmethod
    def get_user_assets_class():
        return UserAssets

    @classmethod
    def _create_obj(cls, **kwargs):
        db[User.table_name].insert_one(kwargs)

    def _update_obj(self, **kwargs):
        db[User.table_name].update_one({'id': self._id}, {'$set': {key: val} for key, val in kwargs.items()})

    @classmethod
    def _retrieve_obj(cls, **kwargs) -> dict:
        return db[User.table_name].find_one(kwargs)

    def _get_obj_attr(self, key) -> Any:
        return db[User.table_name].find_one({'id': self._id})[key]

    @classmethod
    def _list_objs(cls, **kwargs) -> List[dict]:
        return db[User.table_name].find(kwargs)

    def _delete_obj(self):
        db[User.table_name].delete_one({'id': self._id})
