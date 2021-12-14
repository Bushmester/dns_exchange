import pytest

from dns_exchange.models.mongo.users import User
from dns_exchange.handlers import accounts


def get_user(is_admin=False, auth_token=False):
    result = {}

    user = User.create(is_admin=is_admin)
    user.save()

    result['user'] = user

    if auth_token:
        seed_phrase = user.seed_phrase
        response_from_import = accounts.import_account(seed_phrase=seed_phrase, auth_token='')
        auth_token = response_from_import.auth_token
        result['auth_token'] = auth_token

    return result
