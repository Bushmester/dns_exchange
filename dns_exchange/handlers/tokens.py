from datetime import datetime
from typing import Union

from dns_exchange.handlers.helpers import admin_required, auth_required, StopTransaction
from dns_exchange.helpers import Response
from dns_exchange.models.mongo.common import DBTransaction
from dns_exchange.models.mongo.token_pairs import BuyOrder, SellOrder, TokenPair
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


def perform_transfer(user_from: User, user_to: User, token: str, amount: float) -> None:
    # Withdraw token from user_from
    user_from.assets[token] = user_from.assets[token] - amount
    user_from.save()

    # Deposit token to user_to
    user_to_assets_dict = dict(user_to.assets)
    if token in user_to_assets_dict:
        user_to.assets[token] = user_to_assets_dict[token] + amount
    else:
        user_to.assets[token] = amount
    user_to.save()

    # Create user_from to user_to transaction record
    Transaction.create(
        date=datetime.utcnow(),
        from_=user_from.address,
        to=user_to.address,
        token=token,
        amount=amount
    ).save()


def get_response_about_exchange_token(
        action: str,
        user: User,
        data: Union[BuyCommandData, SellCommandData]
):
    token1, token2 = data.trading_pair.split('_')
    response_lines = []

    if action == 'buy':
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

    amount_left = data.amount

    for order in orders:
        if amount_left > 0:
            order_exchange_rate = order.exchange_rate
            order_amount = order.amount
            order_user = User.retrieve(address=order.address)

            token1_receiver = user if action == 'buy' else order_user
            token1_sender = order_user if action == 'buy' else user

            try:
                with DBTransaction():
                    # If order filled fully
                    if amount_left >= order_amount:
                        token1_amount = order_amount
                        order.delete()
                    # If order filled partially
                    else:
                        token1_amount = amount_left
                        order.amount = order.amount - amount_left

                    token2_amount = token1_amount * order_exchange_rate

                    perform_transfer(token1_sender, token1_receiver, token=token1, amount=token1_amount)
                    perform_transfer(token1_receiver, token1_sender, token=token2, amount=token2_amount)

                    token1_sender_legit = token1_sender.assets[token1] > 0
                    token1_receiver_legit = token1_receiver.assets[token2] > 0

                    if all([token1_sender_legit, token1_receiver_legit]):
                        response_lines.append(
                            f'{"Bought" if action == "buy" else "Sold"} {token1_amount} {token1} ({order_exchange_rate} '
                            f'{token2} per 1 {token1})'
                        )
                        amount_left -= token1_amount
                    else:
                        raise StopTransaction('Asset amount can\'t be negative!')
            except ValueError:
                pass

            if not token1_sender_legit:
                order.delete()

        else:
            break

    if amount_left > 0 and data.exchange_rate is not None:
        (BuyOrder if action == 'buy' else SellOrder).create(
            pair_label=data.trading_pair,
            exchange_rate=data.exchange_rate,
            amount=amount_left,
            address=user.address
        ).save()

        response_lines.append(
            f'Placed {amount_left} {token1} {"buy" if action == "buy" else "sell"} order '
            f'({data.exchange_rate} {token2} per 1 {token1})'
        )

    return response_lines


@auth_required
def buy(user, **kwargs):
    data = BuyCommandData(**kwargs)
    response = Response()

    try:
        TokenPair.retrieve(label=data.trading_pair)
    except TypeError:
        return Response(errors=["Pair label is incorrect!"])

    token1, token2 = data.trading_pair.split('_')

    # Check that user has enough tokens for the deal
    is_min_amount_satisfied = False
    try:
        is_min_amount_satisfied = user.assets[token2] >= data.amount * data.exchange_rate
    except KeyError:
        pass
    if not is_min_amount_satisfied:
        return Response(errors=[f'You don\'t have enough {token2} to buy {token1}!'])

    response.add_content_text(
        lines=get_response_about_exchange_token(
            action="buy",
            user=user,
            data=data
        )
    )

    return response


@auth_required
def sell(user, **kwargs):
    data = SellCommandData(**kwargs)
    response = Response()

    try:
        TokenPair.retrieve(label=data.trading_pair)
    except TypeError:
        return Response(errors=["Pair label is incorrect!"])

    token1, token2 = data.trading_pair.split('_')

    # Check that user has enough tokens for the deal
    is_min_amount_satisfied = False
    try:
        is_min_amount_satisfied = user.assets[token1] >= data.amount
    except KeyError:
        pass
    if not is_min_amount_satisfied:
        return Response(errors=[f'You don\'t have enough {token1}!'])

    response.add_content_text(
        lines=get_response_about_exchange_token(
            action="sell",
            user=user,
            data=data
        )
    )

    return response
