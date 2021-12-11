from typing import Any, List

from bson import ObjectId

from dns_exchange.models.interfaces.users import UserAssetsInterface, UserInterface, get_address, get_seed_phrase
from dns_exchange.database import db


class UserAssets:
    field_name = 'assets'

    def __init__(self, owner_id):
        self._owner_id = owner_id
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
        db[User.table_name].update_one({'id': self._owner_id.id}, {'$set': {f'{UserAssets.field_name}.{key}': value}})

    def _get_value(self, key: str):
        return db[User.table_name].find_one({'id': self._owner_id.id})[UserAssets.field_name][key]

    def _delete_value(self, key: str):
        db[User.table_name].update_one({'id': self._owner_id.id}, {'$unset': {f'{UserAssets.field_name}.{key}': None}})


class User:
    table_name = 'users'
    descriptor_attrs = ('assets',)

    def __init__(self, obj_id, is_new, **kwargs):
        self._id = obj_id
        self._is_new = is_new
        self._attrs_to_save = {**kwargs}

        self._assets = UserAssets(self)

    @staticmethod
    def get_default_kwargs(**kwargs):
        return {
            'id': str(ObjectId()),
            'address': get_address(),
            'seed_phrase': get_seed_phrase(),
            'is_admin': False,
            **kwargs
        }

    """Interface to work with"""

    @classmethod
    def create(cls, **kwargs):
        default_kwargs = cls.get_default_kwargs(**kwargs)
        odj_id = default_kwargs.pop('id')
        return cls(cls.get_default_kwargs(**kwargs), obj_id=odj_id, is_new=True)

    @classmethod
    def retrieve(cls, **kwargs):
        obj_id = kwargs['id'] if 'id' in kwargs.keys() else cls._retrieve_obj(**kwargs)['id']
        return cls(obj_id=obj_id, is_new=False)

    def __getattr__(self, key):
        if key in self.descriptor_attrs:
            getattr(self, f'_{key}')
        return self._get_obj_attr(key)

    def __setattr__(self, key, value):
        if key in self.descriptor_attrs:
            raise AttributeError('You can\'t set this attribute explicitly')
        if key[0] == '_':
            super().__setattr__(key, value)
        else:
            self._attrs_to_save[key] = value

    def save(self):
        if self._is_new:
            self._create_obj(**self._attrs_to_save)
            self._is_new = False
        else:
            self._update_obj(**self._attrs_to_save)
        self._assets.save()

    def delete(self):
        self._delete_obj()
        del self

    """Methods that make interface work"""

    @classmethod
    def _create_obj(cls, **kwargs):
        db[User.table_name].insert_one({key: val for key, val in kwargs.items()})

    def _update_obj(self, **kwargs):
        db[User.table_name].update_one({'id': self._id}, {'$set': {key: val} for key, val in kwargs.items()})

    @classmethod
    def _retrieve_obj(cls, **kwargs) -> dict:
        return db[User.table_name].find_one({key: val for key, val in kwargs.items()})

    def _get_obj_attr(self, key) -> Any:
        return db[User.table_name].find_one({'id': self._id})[key]

    @classmethod
    def _list_objs(cls, **kwargs) -> List[dict]:
        pass

    def _delete_obj(self):
        db[User.table_name].delete_one({'id': self._id})
