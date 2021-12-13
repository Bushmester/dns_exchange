import pytest

from dns_exchange.models.mongo.users import User
from dns_exchange.handlers import accounts


class CustomUser(User):

    def __init__(self, obj_id, is_new, **kwargs):
        super().__init__(obj_id, is_new, **kwargs)
        self.auth_token = None

    @property
    def auth_token(self):
        return self.auth_token

    @auth_token.setter
    def auth_token(self, value):
        self.auth_token = value


def get_user(is_admin=False, auth_token=False):
    result = {}

    user = CustomUser.create(is_admin=is_admin)
    user.save()

    result['user'] = user

    if auth_token:
        seed_phrase = user.seed_phrase
        response_from_import = accounts.import_account(seed_phrase=seed_phrase, auth_token='')
        auth_token = response_from_import.auth_token
        result['auth_token'] = auth_token

    return result


def clean_db(lst_with_objects: list):
    for obj in lst_with_objects:
        obj.delete()
