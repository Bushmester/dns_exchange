from datetime import datetime
from typing import Union

from dns_exchange.handlers.tokens import BuyCommandData, SellCommandData
from dns_exchange.models.mongo.common import DBTransaction
from dns_exchange.models.mongo.token_pairs import SellOrder, BuyOrder
from dns_exchange.models.mongo.transactions import Transaction
from dns_exchange.models.mongo.users import User

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
        check = ""
        try:
            check = user.assets[give_token]
        except KeyError:
            pass
        if (check is None) or (check < data.amount * data.exchange_rate):
            return response.append(f'You do not have enough {give_token} to buy {receiver_token}!')

        if isinstance(data, BuyCommandData):
            orders = list(
                filter(
                    lambda x: x.exchange_rate <= data.exchange_rate if data.exchange_rate is not None else True,
                    sorted(orders_classes[func].list(pair_label=data.trading_pair), key=lambda x: x.exchange_rate)
                )
            )
        else:
            list(
                filter(
                    lambda x: x.exchange_rate >= data.exchange_rate if data.exchange_rate is not None else True,
                    sorted(orders_classes[func].list(pair_label=data.trading_pair), key=lambda x: x.exchange_rate)
                )
            )

        for order in orders:
            if data.amount > 0:
                order_exchange_rate = order.exchange_rate
                order_amount = order.amount
                receiver = user if isinstance(data, SellCommandData) else User.retrieve(address=order.address)
                giver = user if isinstance(data, BuyCommandData) else User.retrieve(address=order.address)

                # If order filled fully
                if data.amount >= order_amount:
                    receiver_token_amount = order_amount
                    order.delete()
                # If order filled partially
                else:
                    receiver_token_amount = data.amount
                    order.amount = order.amount - data.amount

                give_token_amount = receiver_token_amount * order_exchange_rate

                perform_transfer(giver, receiver, receiver_token, receiver_token_amount)
                perform_transfer(receiver, giver, give_token, give_token_amount)

                giver_legit = giver.asstets[receiver_token] > 0
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
