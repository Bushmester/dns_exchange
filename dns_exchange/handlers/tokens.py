from datetime import datetime
from typing import Union, List

from dns_exchange.config import COMMISSION
from dns_exchange.handlers.helpers import admin_required, auth_required
from dns_exchange.helpers import Response
from dns_exchange.models.interfaces.errors import StopTransaction
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
    response.add_content_text(title=f'You\'ve received {data.quantity} {data.tag} tokens!')

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
    amount = amount * (1 - COMMISSION)
    user_to.assets[token] = user_to_assets_dict[token] + amount if token in user_to_assets_dict else amount
    user_to.save()

    # Create user_from to user_to transaction record
    Transaction.create(
        date=datetime.utcnow(),
        from_=user_from.address,
        to=user_to.address,
        token=token,
        amount=amount
    ).save()


def get_exchange_token_response_lines(
        action: str,
        user: User,
        data: Union[BuyCommandData, SellCommandData]
) -> List[str]:
    # main_token is the first token of the pair (e.g. "BTC" in "BTC_ETH" pair)
    # second_token is the second token of the pair (e.g. "ETH" in "BTC_ETH" pair)
    # The reason to use these definitions because terms buy/sell are applied to the first (main)
    # token of the pair (e.g. in pair "BTC_ETH" we buy or sell BTC for ETH, there is no such
    # operation as "buy ETH", because that simply means "sell BTC")
    main_token, second_token = data.trading_pair.split('_')
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

            buyer = user if action == 'buy' else order_user
            seller = order_user if action == 'buy' else user

            try:
                with DBTransaction():
                    # If order filled fully
                    if amount_left >= order_amount:
                        main_token_amount = order_amount
                        order.delete()
                    # If order filled partially
                    else:
                        main_token_amount = amount_left
                        order.amount = order.amount - amount_left

                    second_token_amount = main_token_amount * order_exchange_rate

                    perform_transfer(seller, buyer, token=main_token, amount=main_token_amount)
                    perform_transfer(buyer, seller, token=second_token, amount=second_token_amount)

                    is_main_token_sender_legit = seller.assets[main_token] > 0
                    is_main_token_receiver_legit = buyer.assets[second_token] > 0

                    if all([is_main_token_sender_legit, is_main_token_receiver_legit]):
                        response_lines.append(
                            f'{"Bought" if action == "buy" else "Sold"} {main_token_amount} {main_token} '
                            f'({order_exchange_rate} {second_token} per 1 {main_token})'
                        )
                        amount_left -= main_token_amount
                    else:
                        raise StopTransaction('Asset amount can\'t be negative!')
            except StopTransaction:
                pass

            if not is_main_token_sender_legit:
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
            f'Placed {amount_left} {main_token} {"buy" if action == "buy" else "sell"} order '
            f'({data.exchange_rate} {second_token} per 1 {main_token})'
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

    main_token, second_token = data.trading_pair.split('_')

    # Check that user has enough tokens for the deal
    is_min_amount_satisfied = False
    try:
        is_min_amount_satisfied = user.assets[second_token] >= data.amount * data.exchange_rate
    except KeyError:
        pass
    if not is_min_amount_satisfied:
        return Response(errors=[f'You don\'t have enough {second_token} to buy {main_token}!'])

    response.add_content_text(
        lines=get_exchange_token_response_lines(
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

    main_token, second_token = data.trading_pair.split('_')

    # Check that user has enough tokens for the deal
    is_min_amount_satisfied = False
    try:
        is_min_amount_satisfied = user.assets[main_token] >= data.amount
    except KeyError:
        pass
    if not is_min_amount_satisfied:
        return Response(errors=[f'You don\'t have enough {main_token}!'])

    response.add_content_text(
        lines=get_exchange_token_response_lines(
            action="sell",
            user=user,
            data=data
        )
    )

    return response
