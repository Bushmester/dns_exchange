from abc import ABC
from datetime import datetime

from dns_exchange.models.interfaces.common import BaseModelInterface


class TransactionInterface(BaseModelInterface, ABC):
    model_name = 'transactions'
    required_attrs = {'from_': str, 'to': str, 'token': str, 'amount': float}

    @classmethod
    def get_default_kwargs(cls, **kwargs):
        return {
            'date': datetime.utcnow(),
            **super().get_default_kwargs(**kwargs)
        }
