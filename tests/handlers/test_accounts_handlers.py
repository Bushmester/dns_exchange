from dns_exchange.handlers import accounts
from dns_exchange.models.mongo.users import User
from dns_exchange.dictionaries import auth_dict


def test_create_account():
    res = accounts.create_account(auth_token='')

    address = res.__dict__['content'][0]['lines'][0].replace('address: ', '')
    seed_phrase = res.__dict__['content'][0]['lines'][1].replace('seed_phrase: ', '')

    result = User.retrieve(address=address)
    seed_phrase_from_db = result.seed_phrase

    assert seed_phrase == seed_phrase_from_db


def test_import_account():
    response_from_create = accounts.create_account(auth_token='')
    seed_phrase = response_from_create.__dict__['content'][0]['lines'][1].replace('seed_phrase: ', '')

    response_from_import = accounts.import_account(seed_phrase=seed_phrase, auth_token='')
    auth_token = response_from_import.__dict__['auth_token']

    seed_phrase_from_auth_dict = auth_dict[auth_token].seed_phrase

    assert seed_phrase_from_auth_dict == seed_phrase


def test_my_account():
    response_from_create = accounts.create_account(auth_token='')
    address = response_from_create.__dict__['content'][0]['lines'][0].replace('address: ', '')
    seed_phrase = response_from_create.__dict__['content'][0]['lines'][1].replace('seed_phrase: ', '')

    response_from_import = accounts.import_account(seed_phrase=seed_phrase, auth_token='')
    auth_token = response_from_import.__dict__['auth_token']

    response_from_my_account = accounts.my_account(auth_token=auth_token)
    address_from_my_account = response_from_my_account.__dict__['content'][0]['lines'][0].replace('address: ', '')

    assert address_from_my_account == address


def test_account_info():
    response_from_create = accounts.create_account(auth_token='')
    address = response_from_create.__dict__['content'][0]['lines'][0].replace('address: ', '')

    response_from_account_info = accounts.account_info(address=address, auth_token='', number=1)

    assert response_from_account_info





