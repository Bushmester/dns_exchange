from abc import ABC

from dns_exchange.models.interfaces.common import BaseModelInterface


class TransactionInterface(BaseModelInterface, ABC):
    model_name = 'transactions'
