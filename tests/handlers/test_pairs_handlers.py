import pytest

from tests import helpers
from dns_exchange.handlers import pairs, accounts
from dns_exchange.models.mongo.users import User
from dns_exchange.models.mongo.token_pairs import TokenPair


@pytest.mark.usefixtures("clean_db")
def test_add_pairs():

    user_info = helpers.get_user(is_admin=True, auth_token=True)
    user = user_info['user']
    auth_token = user_info['auth_token']

    token1 = 'STS'
    token2 = 'TNT'
    label = f'{token1}_{token2}'

    response_from_add_pair = pairs.add_pair(token1=token1, token2=token2, auth_token=auth_token)

    pair_from_db = TokenPair.retrieve(label=label)
    label_from_db = pair_from_db.label

    assert label == label_from_db


@pytest.mark.usefixtures("clean_db")
def test_delete_pairs():

    user_info = helpers.get_user(is_admin=True, auth_token=True)
    user = user_info['user']
    auth_token = user_info['auth_token']

    label = "KTK_PTK"
    token_pair = TokenPair.create(label=label)
    token_pair.save()

    response_from_delete_pair = pairs.delete_pair(label=label, auth_token=auth_token)

    try:
        pair_from_db = TokenPair.retrieve(label=label)
    except TypeError:
        pair_from_db = None

    assert pair_from_db is None


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
