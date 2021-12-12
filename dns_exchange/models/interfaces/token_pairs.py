from abc import abstractmethod, ABC

from dns_exchange.models.interfaces.common import BaseModelInterface, BaseModelListOfDictsField


class TokenPairBuyOrders(BaseModelListOfDictsField, ABC):
    attr_name = 'buy_orders'


class TokenPairInterface(BaseModelInterface, ABC):
    model_name = 'token_pairs'
    complex_attrs = ('buy_orders', 'sell_orders')

    def __init__(self, obj_id, is_new, **kwargs):
        super().__init__(obj_id, is_new, **kwargs)
        self._buy_orders = self.get_buy_orders_class()(self._id, self.model_name)
        self._sell_orders = self.get_sell_orders_class()(self._id, self.model_name)

    def save_complex_attrs(self):
        self._buy_orders.save()
        self._sell_orders.save()

    @staticmethod
    @abstractmethod
    def get_buy_orders_class():
        pass

    @staticmethod
    @abstractmethod
    def get_sell_orders_class():
        pass
