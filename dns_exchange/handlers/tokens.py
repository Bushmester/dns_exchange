from _ast import pattern
from datetime import datetime

from dns_exchange.handlers.helpers import admin_required, auth_required
from dns_exchange.helpers import Response
from dns_exchange.models.mongo.common import DBTransaction
from dns_exchange.models.mongo.token_pairs import SellOrder, BuyOrder
from dns_exchange.models.mongo.transactions import Transaction
from dns_exchange.models.mongo.users import User
from dns_exchange.validators import String, FloatNumber


# Helpers
def perform_transfer(user_from: User, user_to: User, token_tag: str, amount: float) -> None:
    # Withdraw token_tag from user_from
    user_from.assets[token_tag] = user_from.assets[token_tag] - amount
    user_from.save()

    # Deposit token_tag to user_to
    user_to_assets_dict = dict(user_to.assets)
    if token_tag in user_to_assets_dict:
        user_to.assets[token_tag] = user_to_assets_dict[token_tag] + amount
    else:
        user_to.assets[token_tag] = amount
    user_to.save()

    # Create user_from to user_to transaction record
    Transaction.create(
        date=datetime.utcnow(),
        from_=user_from.address,
        to=user_to.address,
        token=token_tag,
        amount=amount
    ).save()


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
    response.add_content_text(title=f'You\'ve recieved {data.quantity} {data.tag} tokens!')
    user.save()

    return response


# buy command
class BuyCommandData:
    trading_pair = String(pattern=r'[A-Z]{3,4}_[A-Z]{3,4}')
    amount = FloatNumber(minvalue=0.1)
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

    sell_orders = list(
        filter(
            lambda x: x.exchange_rate <= data.exchange_rate if data.exchange_rate is not None else True,
            sorted(SellOrder.list(pair_label=data.trading_pair), key=lambda x: x.exchange_rate)
        )
    )

    for sell_order in sell_orders:
        if data.amount > 0:
            order_exchange_rate = sell_order.exchange_rate
            order_amount = sell_order.amount
            buyer = user
            seller = User.retrieve(address=sell_order.address)
            token1, token2 = data.trading_pair.split('_')

            with DBTransaction:
                # If order filled fully
                if data.amount >= order_amount:
                    token1_amount = order_amount
                    sell_order.delete()
                # If order filled partially
                else:
                    token1_amount = data.amount
                    sell_order.amount = sell_order.amount - data.amount

                token2_amount = token1_amount * order_exchange_rate

                perform_transfer(seller, buyer, token1, token1_amount)
                perform_transfer(buyer, seller, token2, token2_amount)

                # Check if buyer and seller balances are positive
                seller_legit = seller.assets[token1] > 0
                buyer_legit = buyer.assets[token2] > 0

                if not all([seller_legit, buyer_legit]):
                    raise ValueError('Asset amount can\'t be negative!')

            # Delete order if seller unable to perform operation
            if not seller_legit:
                sell_order.delete()

            data.amount -= token1_amount

        else:
            break

    # Place buy order if needed
    if data.amount > 0 and data.exchange_rate is not None:
        BuyOrder.create(
            pair_label=data.trading_pair,
            exchange_rate=data.exchange_rate,
            amount=data.amount,
            address=user.address
        )

    # TODO: Add response text

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
    # TODO: Sell logic
    return response
