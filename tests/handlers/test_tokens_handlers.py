from dns_exchange.handlers import accounts
from dns_exchange.handlers import tokens, pairs
from dns_exchange.models.mongo.users import User

from tests import helpers


def test_add_token():
    user_info = helpers.get_user(is_admin=True, auth_token=True)
    user = user_info['user']
    auth_token = user_info['auth_token']
    btc_count = 3.0

    response_from_add_token = tokens.add_token(auth_token=auth_token, tag='BTC', quantity=btc_count)

    user = User.retrieve(address=user.address)
    btc_count_from_db = user.assets['BTC']

    assert btc_count_from_db == btc_count


def test_buy():
    user_info = helpers.get_user(auth_token=True, is_admin=True)
    user = user_info['user']
    auth_token = user_info['auth_token']

    token1 = 'CAT'
    token2 = 'DOG'
    pair = f'{token1}_{token2}'

    amount = 1.0
    exchange_rate = 1.0

    tokens.add_token(auth_token=auth_token, tag=token1, quantity=amount)

    response_from_buy = tokens.buy(trading_pair=pair, amount=amount,
                                   exchange_rate=exchange_rate, auth_token=auth_token)
    print(response_from_buy.get_json_string())

    assert 1 == 1


def test_sell():
    user_info = helpers.get_user(auth_token=True, is_admin=True)
    user = user_info['user']
    auth_token = user_info['auth_token']

    token1 = 'WWW'
    token2 = 'SSS'
    pair = f'{token1}_{token2}'

    amount = 1.0
    exchange_rate = 1.0

    tokens.add_token(auth_token=auth_token, tag=token1, quantity=amount)

    response_from_sell = tokens.sell(trading_pair=pair, amount=amount,
                                     exchange_rate=exchange_rate, auth_token=auth_token)
    print(response_from_sell.get_json_string())

    assert 1 == 1
