from abc import ABC

from dns_exchange.models.interfaces.common import BaseModelInterface


class BuyOrderInterface(BaseModelInterface, ABC):
    model_name = 'buy_orders'
    required_attrs = {'pair_label': str, 'exchange_rate': float, 'amount': float, 'address': str}


class SellOrderInterface(BaseModelInterface, ABC):
    model_name = 'sell_orders'
    required_attrs = {'pair_label': str, 'exchange_rate': float, 'amount': float, 'address': str}


class TokenPairInterface(BaseModelInterface, ABC):
    model_name = 'token_pairs'
    required_attrs = {'label': str}
