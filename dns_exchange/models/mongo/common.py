from abc import ABC
from typing import Any, List

from dns_exchange.models.interfaces.common import (
    BaseModelDictFieldInterface, BaseModelInterface,
    DBTransactionInterface,
)
from dns_exchange.database import db


def run_with_transaction(func, *args, **kwargs):
    with db.start_session() as session:
        with session.start_transaction():
            return func(*args, **kwargs)


class DBTransaction(DBTransactionInterface):
    def __init__(self):
        self.transaction = None

    def enter(self):
        session = db.start_session()
        self.transaction = session.start_transaction()
        return self.transaction

    def exit(self):
        self.transaction.__exit__()
        db.close()


class BaseModelDictField(BaseModelDictFieldInterface, ABC):
    def _set_value(self, key: str, value: Any):
        db[self._owner_model_name].update_one({'id': self._owner_id}, {'$set': {f'{self.attr_name}.{key}': value}})

    def _get_value(self, key: str):
        return db[self._owner_model_name].find_one({'id': self._owner_id})[self.attr_name][key]

    def _delete_value(self, key: str):
        db[self._owner_model_name].update_one({'id': self._owner_id}, {'$unset': {f'{self.attr_name}.{key}': None}})

    def _list_values(self):
        return db[self._owner_model_name].find_one({'id': self._owner_id})[self.attr_name]


class BaseModel(BaseModelInterface, ABC):
    @classmethod
    def _create_obj(cls, **kwargs):
        db[cls.model_name].insert_one(kwargs)

    def _update_obj(self, **kwargs):
        db[self.model_name].update_one({'id': self._id}, {'$set': {key: val} for key, val in kwargs.items()})

    @classmethod
    def _retrieve_obj(cls, **kwargs) -> dict:
        return db[cls.model_name].find_one(kwargs)

    def _get_obj_attr(self, key) -> Any:
        return db[self.model_name].find_one({'id': self._id})[key]

    @classmethod
    def _list_objs(cls, **kwargs) -> List[dict]:
        return db[cls.model_name].find(kwargs)

    def _delete_obj(self):
        db[self.model_name].delete_one({'id': self._id})
