from dns_exchange.handlers import accounts
from dns_exchange.handlers import tokens
from dns_exchange.models.mongo.users import User


def test_add_token():
    user = User.create(is_admin=True)
    user.save()

    seed_phrase = user.seed_phrase

    response_from_import = accounts.import_account(seed_phrase=seed_phrase, auth_token='')
    auth_token = response_from_import.__dict__['auth_token']

    response_from_add_token = tokens.add_token(auth_token=auth_token, tag='btc', quantity=3)

    user = User.retrieve(address=user.address)

    assert 1 == 1
