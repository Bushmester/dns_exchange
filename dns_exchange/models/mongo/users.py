from typing import Any, List

from bson import ObjectId

from dns_exchange.models.interfaces.users import UserAssetsInterface, UserInterface, get_address, get_seed_phrase
from dns_exchange.database import db


class UserAssets:
    field_name = 'assets'

    def __init__(self, owner_id):
        self.owner_id = owner_id
        self._assets_to_save = {}

    """Interface to work with"""

    def __setitem__(self, key, value):
        self._assets_to_save[key] = value

    def __getitem__(self, key):
        return self._get_value(key)

    def __delitem__(self, key):
        self._delete_value(key)

    def save(self):
        for key, val in self._assets_to_save.items():
            self._set_value(key, val)
        self._assets_to_save = {}

    """Methods that make interface work"""

    def _set_value(self, key: str, value: Any):
        db[User.table_name].update_one({'id': self.owner_id.id}, {'$set': {f'{UserAssets.field_name}.{key}': value}})

    def _get_value(self, key: str):
        return db[User.table_name].find_one({'id': self.owner_id.id})[UserAssets.field_name][key]

    def _delete_value(self, key: str):
        db[User.table_name].update_one({'id': self.owner_id.id}, {'$unset': {f'{UserAssets.field_name}.{key}': None}})


class User:
    # Attributes below must be specified by ModelInterface
    table_name = 'users'
    # __slots__ = ('id', 'address', 'seed_phrase', 'is_admin', 'assets')

    fields_to_change = ('id', 'address', 'seed_phrase')

    def __init__(self, id=None, address=None, seed_phrase=None, is_new=None, **kwargs):
        self._is_new = is_new

        self.id = id if id else str(ObjectId())
        self.address = address if address else get_address()
        self.seed_phrase = seed_phrase if seed_phrase else get_seed_phrase()

        self.is_admin = False
        self.assets = UserAssets(self)

    """Interface to work with"""

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs, is_new=True)

    @classmethod
    def retrieve(cls, **kwargs):
        obj_data = cls._retrieve_obj(**kwargs)
        return cls(**obj_data, is_new=False)

    def save(self):
        kwargs = {key: getattr(self, key) for key in self.fields_to_change}
        if self._is_new:
            self._create_obj(**kwargs)
            self._is_new = False
        else:
            self._update_obj(**kwargs)
        self.assets.save()

    def delete(self):
        self._delete_obj()
        del self

    """Methods that make interface work"""

    @classmethod
    def _create_obj(cls, **kwargs):
        db[User.table_name].insert_one({key: val for key, val in kwargs.items()})

    def _update_obj(self, **kwargs):
        db[User.table_name].update_one({'id': self.id}, {'$set': {key: val} for key, val in kwargs.items()})

    @classmethod
    def _retrieve_obj(cls, **kwargs) -> dict:
        return db[User.table_name].find_one({key: val for key, val in kwargs.items()})

    @classmethod
    def _list_objs(cls, **kwargs) -> List[dict]:
        pass

    def _delete_obj(self):
        db[User.table_name].delete_one({'id': self.id})
