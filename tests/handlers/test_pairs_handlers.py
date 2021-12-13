from dns_exchange.handlers import pairs, accounts
from dns_exchange.models.mongo.users import User
from dns_exchange.models.mongo.token_pairs import TokenPair


def test_add_pairs():
    user = User.create(is_admin=True)
    user.save()

    seed_phrase = user.seed_phrase

    response_from_import = accounts.import_account(seed_phrase=seed_phrase, auth_token='')
    auth_token = response_from_import.auth_token

    token1 = 'BTC'
    token2 = 'ETH'
    pair = f'{token1}_{token2}'

    response_from_pairs = pairs.add_pair(token1=token1, token2=token2, auth_token=auth_token)

    if response_from_pairs.errors:
        assert response_from_pairs.errors[0] == "Pair already exists!"
        return

    pair_from_db = response_from_pairs.content[0]['title'].split()[0]

    assert pair == pair_from_db
