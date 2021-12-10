from abc import ABC, abstractmethod

from dns_exchange.models.interfaces.common import BaseModelInterface, BaseDescriptorInterface


class UserAssetsInterface(BaseDescriptorInterface, ABC):
    field_name = 'assets'


class UserInterface(BaseModelInterface, ABC):
    table_name = 'users'
    __slots__ = ('id', 'address', 'seed_phrase', 'is_admin', 'assets')

    def __init__(self, address, seed_phrase):
        super().__init__(assets={})
        self.address = address  # TODO: Generate address '0x9c3f7c50'
        self.seed_phrase = seed_phrase  # TODO: Generate seed_phrase 'red blue green yellow orange dick'
        self.is_admin = False
        self.__class__.assets = self._get_assets_descriptor_obj()

    @staticmethod
    @abstractmethod
    def _get_assets_descriptor_obj():
        # Simply uncomment line below
        # return UserAssets()
        pass
