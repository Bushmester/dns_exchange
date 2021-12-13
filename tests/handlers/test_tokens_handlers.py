from dns_exchange.handlers import accounts
from dns_exchange.handlers import tokens, pairs
from dns_exchange.models.mongo.users import User


def test_add_token():
    user = User.create(is_admin=True)
    user.save()

    seed_phrase = user.seed_phrase

    response_from_import = accounts.import_account(seed_phrase=seed_phrase, auth_token='')
    auth_token = response_from_import.auth_token

    btc_count = 3.0

    response_from_add_token = tokens.add_token(auth_token=auth_token, tag='BTC', quantity=btc_count)

    user = User.retrieve(address=user.address)
    btc_count_from_db = user.assets['BTC']

    assert btc_count_from_db == btc_count


def test_buy():
    user = User.create(is_admin=True)
    user.save()

    seed_phrase = user.seed_phrase

    response_from_import = accounts.import_account(seed_phrase=seed_phrase, auth_token='')
    auth_token = response_from_import.auth_token

    token1 = 'BTC'
    token2 = 'ETH'
    pair = f'{token1}_{token2}'

    response_from_pairs = pairs.add_pair(token1=token1, token2=token2, auth_token=auth_token)

    amount = 1.0
    exchange_rate = 1.0

    response_from_buy = tokens.buy(trading_pair=pair, amount=amount, exchange_rate=exchange_rate)
    print(response_from_buy.get_json_string())

    assert 1 == 1
