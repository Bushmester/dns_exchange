import pytest

from dns_exchange.handlers import accounts, tokens
from dns_exchange.models.mongo.transactions import Transaction
from dns_exchange.models.mongo.users import User
from dns_exchange.dictionaries import auth_dict

from tests import helpers


@pytest.mark.usefixtures("clean_db")
def test_create_account():
    res = accounts.create_account(auth_token='')

    address = res.content[0]['lines'][0].replace('address: ', '')
    seed_phrase = res.content[0]['lines'][1].replace('seed_phrase: ', '')

    result = User.retrieve(address=address)
    seed_phrase_from_db = result.seed_phrase

    assert seed_phrase == seed_phrase_from_db


@pytest.mark.usefixtures("clean_db")
def test_import_account():
    user_info = helpers.get_user()
    user = user_info['user']

    response_from_import = accounts.import_account(seed_phrase=user.seed_phrase, auth_token='')
    auth_token = response_from_import.auth_token

    seed_phrase_from_auth_dict = User.retrieve(id=auth_dict[auth_token]).seed_phrase

    assert seed_phrase_from_auth_dict == user.seed_phrase


@pytest.mark.usefixtures("clean_db")
def test_my_account():
    user_info = helpers.get_user()
    user = user_info['user']

    response_from_import = accounts.import_account(seed_phrase=user.seed_phrase, auth_token='')
    auth_token = response_from_import.auth_token

    response_from_my_account = accounts.my_account(auth_token=auth_token)
    address_from_my_account = response_from_my_account.content[0]['lines'][0].replace('address: ', '')

    assert address_from_my_account == user.address


@pytest.mark.usefixtures("clean_db")
def test_account_info():
    user_info = helpers.get_user(is_admin=True, auth_token=True)
    user = user_info['user']
    auth_token = user_info['auth_token']
    tit_count = 3.0

    response_from_add_token = tokens.add_token(auth_token=auth_token, tag='TIT', quantity=tit_count)
    excepted_response_for_token_add = [("TIT", 3.0)]
    response_from_account_info = accounts.account_info(address=user.address, auth_token='', number=1)
    response_for_token_add = response_from_account_info.content[0]["rows"]

    assert str(response_for_token_add) == str(excepted_response_for_token_add)





