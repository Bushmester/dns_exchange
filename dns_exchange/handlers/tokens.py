from datetime import datetime

from dns_exchange.handlers.helpers import admin_required, auth_required
from dns_exchange.helpers import Response
from dns_exchange.models.mongo.common import DBTransaction
from dns_exchange.models.mongo.token_pairs import SellOrder, BuyOrder
from dns_exchange.models.mongo.transactions import Transaction
from dns_exchange.models.mongo.users import User
from dns_exchange.validators import String, FloatNumber


# add_token command
class AddTokenCommandData:
    tag = String(minsize=3, maxsize=4)
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
    # TODO: Add token logic
    return Response()


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


# @auth_required
def buy(user="", **kwargs):
    data = BuyCommandData(**kwargs)
    response = Response()
    user = User.retrieve(address="0x2606cc37")  # TODO: Del this

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

                # Withdraw token1 from seller
                seller.assets[token1] = seller.assets[token1] - token1_amount
                seller.save()

                # Deposit token1 to buyer
                buyer_assets_dict = dict(buyer.assets)
                if token1 in buyer_assets_dict:
                    buyer.assets[token1] = buyer_assets_dict[token1] + token1_amount
                else:
                    buyer.assets[token1] = token1_amount
                buyer.save()

                # Create seller-to-buyer transaction record
                Transaction.create(
                    date=datetime.utcnow(),
                    from_=sell_order.address,
                    to=user.address,
                    token=token1,
                    amount=token1_amount
                ).save()

                # Withdraw token2 from buyer
                buyer.assets[token2] = buyer.assets[token2] - token2_amount
                buyer.save()

                # Deposit token2 to seller
                seller_assets_dict = dict(seller.assets)
                if token2 in seller_assets_dict:
                    seller.assets[token2] = seller_assets_dict[token2] + token2_amount
                else:
                    seller.assets[token2] = token2_amount
                seller.save()

                # Create buyer-to-seller transaction record
                Transaction.create(
                    date=datetime.utcnow(),
                    from_=user.address,
                    to=sell_order.address,
                    token=token2,
                    amount=token2_amount
                ).save()

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
    if data.amount > 0 and data.exchange_rate:
        BuyOrder.create(
            pair_label=data.trading_pair,
            exchange_rate=data.exchange_rate,
            amount=data.amount,
            address=user.address
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
    # TODO: Sell logic
    return response
