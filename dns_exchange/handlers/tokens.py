from dns_exchange.handlers.helpers import admin_required, auth_required
from dns_exchange.helpers import Response
from dns_exchange.validators import String, Number


# add_token command
class AddTokenCommandData:
    tag = String(minsize=3, maxsize=4)
    quantity = Number(minvalue=0)

    def __init__(self, **kwargs):
        # Required arguments
        assert 'tag' in kwargs.keys(), 'command "add_token" requires argument "tag"'
        self.tag = kwargs['tag']

        assert 'quantity' in kwargs.keys(), 'command "add_token" requires argument "quantity"'
        self.quantity = kwargs['quantity']


@admin_required
def add_token(user, **kwargs):
    data = AddTokenCommandData(**kwargs)
    # TODO: Add token logic
    return Response()


# buy command
class BuyCommandData:
    trading_pair = String(minsize=3, maxsize=4)
    amount = Number(minvalue=0)
    exchange_rate = Number(minvalue=0)

    def __init__(self, **kwargs):
        # Required arguments
        assert 'trading_pair' in kwargs.keys(), 'command "buy" requires argument "trading_pair"'
        self.trading_pair = kwargs['trading_pair']

        assert 'amount' in kwargs.keys(), 'command "buy" requires argument "amount"'
        self.amount = kwargs['amount']

        # Optional arguments
        self.exchange_rate = kwargs['exchange_rate'] if 'exchange_rate' in kwargs.keys() else None


@auth_required
def buy(user, **kwargs):
    data = BuyCommandData(**kwargs)
    # TODO: Buy logic
    return Response()


# sell command
class SellCommandData:
    trading_pair = String(minsize=3, maxsize=4)
    amount = Number(minvalue=0)
    exchange_rate = Number(minvalue=0)

    def __init__(self, **kwargs):
        # Required arguments
        assert 'trading_pair' in kwargs.keys(), 'command "sell" requires argument "trading_pair"'
        self.trading_pair = kwargs['trading_pair']

        assert 'amount' in kwargs.keys(), 'command "sell" requires argument "amount"'
        self.amount = kwargs['amount']

        # Optional arguments
        self.exchange_rate = kwargs['exchange_rate'] if 'exchange_rate' in kwargs.keys() else None


@auth_required
def sell(user, **kwargs):
    data = SellCommandData(**kwargs)
    # TODO: Sell logic
    return Response()
