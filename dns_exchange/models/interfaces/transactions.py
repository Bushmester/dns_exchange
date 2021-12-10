from abc import ABC, abstractmethod

from dns_exchange.models.interfaces.common import BaseModelInterface


class TransactionsInterface(BaseModelInterface, ABC):
    table_name = 'transactions'
    __slots__ = ('id', 'date', 'from', 'to', 'token', 'amount')

    def __init__(self, date, user_from, user_to, token, amount):
        super().__init__()
        self.date = date
        self.user_from = user_from
        self.user_to = user_to
        self.token = token
        self.amount = amount
