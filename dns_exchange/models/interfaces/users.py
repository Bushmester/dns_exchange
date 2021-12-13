from abc import ABC, abstractmethod

from dns_exchange.models.interfaces.common import BaseModelInterface, BaseModelDictFieldInterface
from dns_exchange.models.interfaces.helpers import get_user_address, get_user_seed_phrase


class UserAssetsInterface(BaseModelDictFieldInterface, ABC):
    attr_name = 'assets'


class UserInterface(BaseModelInterface, ABC):
    model_name = 'users'
    complex_attrs = ('assets',)
    optional_attrs = {'is_admin': bool}

    def __init__(self, obj_id, is_new, **kwargs):
        super().__init__(obj_id, is_new, **kwargs)
        self._assets = self.get_user_assets_class()(self._id, self.model_name)

    @classmethod
    def get_default_kwargs(cls, **kwargs):
        return {
            'address': get_user_address(),
            'seed_phrase': get_user_seed_phrase(),
            'is_admin': kwargs['is_admin'] if 'is_admin' in kwargs else False,
            'assets': {},
            **super().get_default_kwargs(**kwargs)
        }

    def save_complex_attrs(self):
        self._assets.save()

    @staticmethod
    @abstractmethod
    def get_user_assets_class():
        pass
