from dns_exchange.handlers.exchange_token import get_response_about_exchange_token
from dns_exchange.handlers.helpers import admin_required, auth_required
from dns_exchange.helpers import Response
from dns_exchange.validators import String, FloatNumber


# add_token command
class AddTokenCommandData:
    tag = String(pattern=r'[A-Z]{3,4}')
    quantity = FloatNumber(minvalue=0.0)

    def __init__(self, **kwargs):
        # Required arguments
        assert 'tag' in kwargs.keys(), 'command "add_token" requires argument "tag"'
        self.tag = kwargs['tag']

        assert 'quantity' in kwargs.keys(), 'command "add_token" requires argument "quantity"'
        self.quantity = kwargs['quantity']


@admin_required
def add_token(user, **kwargs):
    data = AddTokenCommandData(**kwargs)
    response = Response()

    user_assets = dict(user.assets)
    user.assets[data.tag] = user_assets[data.tag] + data.quantity if data.tag in user_assets else data.quantity
    user.save()
    response.add_content_text(title=f'You\'ve recieved {data.quantity} {data.tag} tokens!')

    return response


# buy command
class BuyCommandData:
    trading_pair = String(pattern=r'[A-Z]{3,4}_[A-Z]{3,4}')
    amount = FloatNumber(minvalue=0.0)
    exchange_rate = FloatNumber(minvalue=0.1)

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
    response = Response()

    token1, token2 = data.trading_pair.split('_')

    response.add_content_text(
        lines=get_response_about_exchange_token(
            func="buy",
            user=user,
            receiver_token=token1,
            give_token=token2,
            data=data
        )
    )
    return response


# sell command
class SellCommandData:
    trading_pair = String(pattern=r'[A-Z]{3,4}_[A-Z]{3,4}')
    amount = FloatNumber(minvalue=0.1)
    exchange_rate = FloatNumber(minvalue=0.1)

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
    response = Response()

    token1, token2 = data.trading_pair.split('_')

    response.add_content_text(
        lines=get_response_about_exchange_token(
            func="sell",
            user=user,
            receiver_token=token2,
            give_token=token1,
            data=data
        )
    )
    return response
