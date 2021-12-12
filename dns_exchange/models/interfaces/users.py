from abc import ABC, abstractmethod
from random import randrange, sample

import requests

from dns_exchange.models.interfaces.common import BaseModelInterface, BaseModelDictFieldInterface


response = requests.get("https://www.mit.edu/~ecprice/wordlist.10000")
words = response.content.splitlines()


def get_address():
    return str(hex(randrange(0, 4294967295)))


def get_seed_phrase():
    return ' '.join(x.decode('utf-8') for x in sample(words, 8))


class UserAssetsInterface(BaseModelDictFieldInterface, ABC):
    attr_name = 'assets'


class UserInterface(BaseModelInterface, ABC):
    model_name = 'users'
    complex_attrs = ('assets',)

    def __init__(self, obj_id, is_new, **kwargs):
        super().__init__(obj_id, is_new, **kwargs)
        self._assets = self.get_user_assets_class()(self._id, self.model_name)

    @classmethod
    def get_default_kwargs(cls, **kwargs):
        return {
            'address': get_address(),
            'seed_phrase': get_seed_phrase(),
            'is_admin': False,
            'assets': {},
            **super().get_default_kwargs(**kwargs)
        }

    def save_complex_attrs(self):
        self._assets.save()

    @staticmethod
    @abstractmethod
    def get_user_assets_class():
        pass
