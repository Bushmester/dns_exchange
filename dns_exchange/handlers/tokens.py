from datetime import datetime
from typing import Union

from dns_exchange.handlers.helpers import admin_required, auth_required
from dns_exchange.helpers import Response
from dns_exchange.models.mongo.common import DBTransaction
from dns_exchange.models.mongo.token_pairs import BuyOrder, SellOrder
from dns_exchange.models.mongo.transactions import Transaction
from dns_exchange.models.mongo.users import User
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


orders_classes = {
    "buy": BuyOrder,
    "sell": SellOrder
}


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


# receive_token - получить/купить
# give_token - отдать/продать
def get_response_about_exchange_token(
        func: str,
        user: User,
        receiver_token: str,
        give_token: str,
        data: Union[BuyCommandData, SellCommandData]
):
    response = []
    with DBTransaction():
        check = None
        try:
            check = user.assets[give_token]
        except KeyError:
            pass
        if (check is None) or (check == 0) or (check < data.amount * data.exchange_rate):
            return response.append(f'You do not have enough {give_token} to buy {receiver_token}!')

        if isinstance(data, BuyCommandData):
            orders = list(
                filter(
                    lambda x: x.exchange_rate <= data.exchange_rate if data.exchange_rate is not None else True,
                    sorted(SellOrder.list(pair_label=data.trading_pair), key=lambda x: x.exchange_rate)
                )
            )
        else:
            orders = list(
                filter(
                    lambda x: x.exchange_rate >= data.exchange_rate if data.exchange_rate is not None else True,
                    sorted(BuyOrder.list(pair_label=data.trading_pair), key=lambda x: x.exchange_rate)
                )
            )

        for order in orders:
            if data.amount > 0:
                order_exchange_rate = order.exchange_rate
                order_amount = order.amount
                receiver = user if isinstance(data, BuyCommandData) else User.retrieve(address=order.address)
                giver = user if isinstance(data, SellCommandData) else User.retrieve(address=order.address)

                # If order filled fully
                if data.amount >= order_amount:
                    receiver_token_amount = order_amount
                    order.delete()
                # If order filled partially
                else:
                    receiver_token_amount = data.amount
                    order.amount = order.amount - data.amount

                give_token_amount = receiver_token_amount * order_exchange_rate
                print(receiver.address)
                print(giver.address)

                perform_transfer(
                    giver,
                    receiver,
                    token_tag=receiver_token if isinstance(data, BuyCommandData) else give_token,
                    amount=receiver_token_amount if isinstance(data, BuyCommandData) else give_token_amount
                )
                perform_transfer(
                    receiver,
                    giver,
                    token_tag=give_token if isinstance(data, BuyCommandData) else receiver_token,
                    amount=give_token_amount if isinstance(data, BuyCommandData) else receiver_token_amount
                )

                giver_legit = giver.assets[receiver_token] > 0
                receiver_legit = receiver.assets[give_token] > 0

                if all([giver_legit, receiver_legit]):
                    response.append(
                        f'Bought {receiver_token_amount} {receiver_token} ({order_exchange_rate} {give_token} per 1 {receiver_token}) '
                    )
                    data.amount -= receiver_token_amount
                else:
                    raise ValueError('Asset amount can\'t be negative!')

                if not giver_legit:
                    order.delete()

            else:
                break

        if data.amount > 0 and data.exchange_rate is not None:
            orders_classes[func].create(
                pair_label=data.trading_pair,
                exchange_rate=data.exchange_rate,
                amount=data.amount,
                address=user.address
            ).save()
            response.append(
                f'Placed {data.amount} {receiver_token} buy order ({data.exchange_rate} {give_token} per 1 {receiver_token})'
            )

    return response


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
