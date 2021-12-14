from datetime import timedelta
from typing import Union

from dns_exchange.initialization import redis_db
from dns_exchange.models.interfaces.common import AuthDictionaryInterface


class AuthDictionary(AuthDictionaryInterface):
    def __contains__(self, item: Union[str, bytes]):
        return bool(redis_db.get(item))

    def __setitem__(self, key, value):
        redis_db.set(key, value, ex=timedelta(days=1))

    def __getitem__(self, key: Union[str, bytes]):
        el = redis_db.get(key)
        if el:
            return el.decode("utf-8")
        else:
            raise KeyError(f'{key}')

    def __delitem__(self, key: Union[str, bytes]):
        redis_db.delete(key)
