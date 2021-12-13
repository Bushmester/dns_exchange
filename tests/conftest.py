import pytest

from dns_exchange.models.mongo.users import User
from dns_exchange.handlers import accounts


@pytest.fixture()
def get_user(request):
    user = User.create().save()
    seed_phrase = user.seed_phrase

    request.cls.user = user


@pytest.fixture()
def get_user_with_auth_token(request):
    user = User.create().save()
    seed_phrase = user.seed_phrase

    response_from_import = accounts.import_account(seed_phrase=seed_phrase, auth_token='')
    auth_token = response_from_import.auth_token

    request.cls.user = user
    request.cls.auth_token = auth_token


