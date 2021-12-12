from abc import ABC

from dns_exchange.models.interfaces.common import BaseModelInterface


class BuyOrderInterface(BaseModelInterface, ABC):
    model_name = 'buy_orders'


class SellOrderInterface(BaseModelInterface, ABC):
    model_name = 'sell_orders'


class TokenPairInterface(BaseModelInterface, ABC):
    model_name = 'token_pairs'
