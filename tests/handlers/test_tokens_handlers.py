import pytest

from dns_exchange.handlers import tokens, pairs
from dns_exchange.models.mongo.users import User

from tests import helpers


@pytest.mark.usefixtures("clean_db")
def test_add_token():
    user_info = helpers.get_user(is_admin=True, auth_token=True)
    user = user_info['user']
    auth_token = user_info['auth_token']
    btc_count = 3.0

    expected_response_title_result = "You've received 3.0 BTC tokens!"

    response_from_add_token = tokens.add_token(auth_token=auth_token, tag='BTC', quantity=btc_count)
    response_title_result = response_from_add_token.content[0]['title']

    user = User.retrieve(address=user.address)
    btc_count_from_db = user.assets['BTC']

    assert btc_count_from_db == btc_count and response_title_result == expected_response_title_result


@pytest.mark.usefixtures("clean_db")
def test_buy():
    user_info_1 = helpers.get_user(auth_token=True, is_admin=True)
    auth_token_1 = user_info_1['auth_token']
    user_1 = user_info_1['user']

    user_info_2 = helpers.get_user(auth_token=True, is_admin=True)
    auth_token_2 = user_info_2['auth_token']
    user_2 = user_info_2['user']

    token1 = 'CAT'
    token2 = 'DOG'
    pair = f'{token1}_{token2}'

    pairs.add_pair(auth_token=auth_token_1, token1=token1, token2=token2)

    tokens.add_token(auth_token=auth_token_1, tag=token1, quantity=15.0)
    tokens.add_token(auth_token=auth_token_2, tag=token2, quantity=10.0)

    expected_response_lines_for_buy = ["Placed 5.0 CAT buy order (1.1 DOG per 1 CAT)"]

    expected_balance_for_user_1 = {'CAT': 10.0, 'DOG': 5.4945}
    expected_balance_for_user_2 = {'DOG': 4.5, 'CAT': 4.995}

    response_from_buy = tokens.buy(trading_pair=pair, amount=5.0, exchange_rate=1.1, auth_token=auth_token_2)
    response_from_sell = tokens.sell(trading_pair=pair, amount=10.0, exchange_rate=1.0, auth_token=auth_token_1)

    response_lines_from_buy = response_from_buy.content[0]['lines']

    balance_for_user_1 = dict(user_1._assets)
    balance_for_user_2 = dict(user_2._assets)

    assert response_lines_from_buy == expected_response_lines_for_buy\
           and balance_for_user_2 == expected_balance_for_user_2\
           and balance_for_user_1 == expected_balance_for_user_1


@pytest.mark.usefixtures("clean_db")
def test_sell():
    user_info_1 = helpers.get_user(auth_token=True, is_admin=True)
    auth_token_1 = user_info_1['auth_token']
    user_1 = user_info_1['user']

    user_info_2 = helpers.get_user(auth_token=True, is_admin=True)
    auth_token_2 = user_info_2['auth_token']
    user_2 = user_info_2['user']

    token1 = 'STS'
    token2 = 'TNT'
    pair = f'{token1}_{token2}'

    pairs.add_pair(auth_token=auth_token_1, token1=token1, token2=token2)

    tokens.add_token(auth_token=auth_token_1, tag=token1, quantity=30.0)
    tokens.add_token(auth_token=auth_token_2, tag=token2, quantity=15.0)

    expected_response_lines_for_sell = ['Sold 5.0 STS (1.4 TNT per 1 STS)',
                                        'Placed 4.0 STS sell order (1.0 TNT per 1 STS)']

    expected_balance_for_user_1 = {'STS': 25.0, 'TNT': 6.993}
    expected_balance_for_user_2 = {'TNT': 8.0, 'STS': 4.995}

    response_from_buy = tokens.buy(trading_pair=pair, amount=5.0, exchange_rate=1.4, auth_token=auth_token_2)
    response_from_sell = tokens.sell(trading_pair=pair, amount=9.0, exchange_rate=1.0, auth_token=auth_token_1)

    response_lines_from_sell = response_from_sell.content[0]['lines']

    balance_for_user_1 = dict(user_1._assets)
    balance_for_user_2 = dict(user_2._assets)

    assert response_lines_from_sell == expected_response_lines_for_sell\
           and balance_for_user_2 == expected_balance_for_user_2\
           and balance_for_user_1 == expected_balance_for_user_1
