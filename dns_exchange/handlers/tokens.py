from dns_exchange.helpers import Response
from dns_exchange.validators import String, Number


# add_token command


class AddTokenCommandData:
    tag = String(minsize=3, maxsize=4)
    quantity = Number(minvalue=0)

    def __init__(self, **kwargs):
        assert len(kwargs) == 2, '"add_token" command takes exactly 2 arguments'
        self.tag = kwargs['tag']
        self.quantity = kwargs['quantity']


def add_token(**kwargs):
    data = AddTokenCommandData(**kwargs)

    # TODO: Add token logic

    return Response()


# buy command


class BuyCommandData:
    trading_pair = String(minsize=3, maxsize=4)
    amount = Number(minvalue=0)
    exchange_rate = Number(minvalue=0)

    def __init__(self, **kwargs):
        assert len(kwargs) == 2, '"buy" command takes minimum 2 and maximum 3 arguments'
        self.trading_pair = kwargs['trading_pair']
        self.amount = kwargs['amount']

        if len(kwargs) > 2:
            self.exchange_rate = kwargs['exchange_rate']


def buy(**kwargs):
    data = BuyCommandData(**kwargs)

    # TODO: Buy logic

    return Response()


# sell command


class SellCommandData:
    trading_pair = String(minsize=3, maxsize=4)
    amount = Number(minvalue=0)
    exchange_rate = Number(minvalue=0)

    def __init__(self, **kwargs):
        assert len(kwargs) == 2, '"sell" command takes exactly 2 arguments'
        self.trading_pair = kwargs['trading_pair']
        self.amount = kwargs['amount']

        if len(kwargs) > 2:
            self.exchange_rate = kwargs['exchange_rate']


def sell(**kwargs):
    data = SellCommandData(**kwargs)

    # TODO: Sell logic

    return Response()
