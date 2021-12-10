from typing import Any

from dns_exchange.models.interfaces.users import UserAssetsInterface, UserInterface
from dns_exchange.dictionaries import db


class UserAssets(UserAssetsInterface):
    @staticmethod
    def _set_value_by_user_id(user_id: int, value: Any):
        list(filter(lambda x: x['id'] == user_id, db[User.table_name]))[0][UserAssets.field_name] = value

    @staticmethod
    def _get_value_by_user_id(user_id: int):
        return list(filter(lambda x: x['id'] == user_id, db[User.table_name]))[0][UserAssets.field_name]


class User(UserInterface):
    @staticmethod
    def _get_assets_descriptor_obj():
        return UserAssets()

    @staticmethod
    def _create_obj(**kwargs):
        db[User.table_name].append(kwargs)

    @staticmethod
    def _retrieve_obj(**kwargs):
        return User.list(**kwargs)[0]

    @staticmethod
    def _list_obj(**kwargs):
        def filter_func(obj):
            for kwarg in kwargs.items():
                if not obj[kwarg[0]] == kwarg[1]:
                    return False
            return True

        return list(filter(filter_func, db[User.table_name]))

    @staticmethod
    def _update_by_id(obj_id: int, field_name: str, value: Any):
        list(filter(lambda x: x['id'] == obj_id, db[User.table_name]))[0][field_name] = value

    @staticmethod
    def _delete_by_id(obj_id: int):
        index = db[User.table_name].index(list(filter(lambda x: x['id'] == obj_id, db[User.table_name]))[0])
        del db[User.table_name][index]
