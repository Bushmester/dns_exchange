from datetime import timedelta
from typing import Union

from dns_exchange.models.dictionaries.common import AuthDictionaryInterface
from dns_exchange.database import redis_db


class RedisAuthDictionary(AuthDictionaryInterface):
    def __contains__(self, item: Union[str, bytes]):
        return True if redis_db.get(item) else False

    def __setitem__(self, key, value):
        redis_db.set(key, value, ex=timedelta(days=1))

    def __getitem__(self, key: Union[str, bytes]):
        if redis_db.get(key):
            return redis_db.get(key).decode("utf-8")
        else:
            raise KeyError(f'{key}')

    def __delitem__(self, key: Union[str, bytes]):
        redis_db.delete(key)
