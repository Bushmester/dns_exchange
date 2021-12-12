from abc import ABC
from datetime import datetime

from dns_exchange.models.interfaces.common import BaseModelInterface


class TransactionInterface(BaseModelInterface, ABC):
    model_name = 'transactions'
    required_attrs = {'date': datetime, 'from': hex, 'to': hex, 'token': str, 'amount': float}
