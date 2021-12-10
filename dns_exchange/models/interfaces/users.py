from abc import ABC, abstractmethod
from hashlib import sha512
from random import randrange, sample

from dns_exchange.models.interfaces.common import BaseModelInterface, BaseDescriptorInterface

import requests

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
WORDS = response.content.splitlines()


def get_address():
    return str(hex(randrange(0, 4294967295)))


def get_seed_phrase():
    seed_phrase = ' '.join(x.decode('utf-8') for x in sample(WORDS, 8))
    return sha512(str.encode(seed_phrase)).hexdigest()


class UserAssetsInterface(BaseDescriptorInterface, ABC):
    field_name = 'assets'


class UserInterface(BaseModelInterface, ABC):
    table_name = 'users'
    __slots__ = ('id', 'address', 'seed_phrase', 'is_admin', 'assets')

    def __init__(self):
        super().__init__(assets={})
        self.address = get_address()
        self.seed_phrase = get_seed_phrase()
        self.is_admin = False
        self.__class__.assets = self._get_assets_descriptor_obj()

    @staticmethod
    @abstractmethod
    def _get_assets_descriptor_obj():
        # Simply uncomment line below
        # return UserAssets()
        pass
