from abc import ABC, abstractmethod

from dns_exchange.models.interfaces.common import BaseModelInterface, BaseDescriptorInterface


class TokenSellOrdersInterface(BaseDescriptorInterface, ABC):
    field_name = 'sell_orders'


class TokenBuyOrdersInterface(BaseDescriptorInterface, ABC):
    field_name = 'buy_orders'


class TokenPairsInterface(BaseModelInterface, ABC):
    table_name = 'tokens_pairs'
    __slots__ = ('id', 'label', 'sell_orders', 'buy_orders')

    def __init__(self, label):
        super().__init__(sell_orders={}, buy_orders={})
        self.label = label
        self.__class__.sell_orders = self._get_sell_orders_descriptor_obj()
        self.__class__.buy_orders = self._get_buy_orders_descriptor_obj()

    @staticmethod
    @abstractmethod
    def _get_sell_orders_descriptor_obj():
        pass

    @staticmethod
    @abstractmethod
    def _get_buy_orders_descriptor_obj():
        pass
