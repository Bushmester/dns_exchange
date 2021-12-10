from abc import ABC, abstractmethod

from dns_exchange.db_models.interfaces.common import BaseModelInterface, BaseDescriptorInterface


class UserAssetsInterface(BaseDescriptorInterface, ABC):
    field_name = 'assets'


class UserInterface(BaseModelInterface, ABC):
    table_name = 'users'
    __slots__ = ('id', 'address', 'seed_phrase', 'is_admin', 'assets')

    def __init__(self):
        super().__init__(assets={})
        self.address = '0x9c3f7c50'  # TODO: Generate address
        self.seed_phrase = 'red blue green yellow orange dick'  # TODO: Generate seed_phrase
        self.is_admin = False
        self.__class__.assets = self._get_assets_descriptor_obj()

    @staticmethod
    @abstractmethod
    def _get_assets_descriptor_obj():
        # Simply uncomment line below
        # return UserAssets()
        pass
