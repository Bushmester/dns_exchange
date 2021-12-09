from dns_exchange.helpers import Response
from dns_exchange.validators import Number


# list_transactions command


class ListTransactionsCommandData:
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        if 'number' in kwargs.keys():
            self.number = kwargs['number']


def list_transactions(**kwargs):
    data = ListTransactionsCommandData(**kwargs)

    # TODO: list_pair logic

    return Response()
