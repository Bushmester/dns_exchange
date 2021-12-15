import pytest

from tests import helpers
from dns_exchange.handlers import pairs, tokens
from dns_exchange.models.mongo.token_pairs import TokenPair, BuyOrder


@pytest.mark.usefixtures("clean_db")
def test_add_pairs():
    user_info = helpers.get_user(is_admin=True, auth_token=True)
    auth_token = user_info['auth_token']

    token1 = 'STS'
    token2 = 'TNT'
    label = f'{token1}_{token2}'

    response_from_add_pair = pairs.add_pair(token1=token1, token2=token2, auth_token=auth_token)

    pair_from_db = TokenPair.retrieve(label=label)
    label_from_db = pair_from_db.label

    except_response_title_result = "STS_TNT pair has been successfully added!"
    response_title_result = response_from_add_pair.content[0]['title']

    assert label == label_from_db and response_title_result == except_response_title_result


@pytest.mark.usefixtures("clean_db")
def test_delete_pairs():
    user_info = helpers.get_user(is_admin=True, auth_token=True)
    auth_token = user_info['auth_token']

    label = "KTK_PTK"
    token_pair = TokenPair.create(label=label)
    token_pair.save()

    response_from_delete_pair = pairs.delete_pair(label=label, auth_token=auth_token)

    except_response_title_result = "KTK_PTK pair has been successfully removed!"
    response_title_result = response_from_delete_pair.content[0]['title']

    try:
        pair_from_db = TokenPair.retrieve(label=label)
    except TypeError:
        pair_from_db = None

    assert pair_from_db is None and except_response_title_result == response_title_result


@pytest.mark.usefixtures("clean_db")
def test_list_pairs():
    filter_by_label = "BTS"
    test_labels = ["BTS_MPS", "BTS_POK", "WER_BTS"]
    for label in test_labels:
        pair = TokenPair.create(label=label)
        pair.save()
    response_from_list_pairs = pairs.list_pairs(auth_token='', filter_by_label=filter_by_label)
    labels_from_db = response_from_list_pairs.content[0]['rows']

    assert labels_from_db == test_labels


@pytest.mark.usefixtures("clean_db")
def test_pair_info():
    user_info = helpers.get_user(is_admin=True, auth_token=True)
    auth_token = user_info['auth_token']

    token1 = 'STS'
    token2 = 'TNT'
    label = f'{token1}_{token2}'

    quantity_token_1 = 12.0

    TokenPair.create(label=label).save()
    tokens.add_token(auth_token=auth_token, tag=token2, quantity=quantity_token_1)

    amount = 11.0
    exchange_rate = 1.0

    tokens.buy(trading_pair=label, amount=amount, exchange_rate=exchange_rate, auth_token=auth_token)

    expected_result = [1.0, 11.0]
    buy_order_from_db = BuyOrder.retrieve(pair_label=label, exchange_rate=exchange_rate, amount=amount)

    response_from_pair_info = pairs.pair_info(auth_token='', label=label)
    result_from_db = response_from_pair_info.content[1]['rows'][0]

    assert expected_result == result_from_db and buy_order_from_db
