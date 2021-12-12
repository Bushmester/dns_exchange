import functools
from uuid import uuid4
from random import uniform, randrange

from dns_exchange.dictionaries import auth_dict


def get_random_mine_number():
    return randrange(1, 10)


def get_random_token_amount():
    return uniform(0, 10)


def generate_auth_token():
    return str(uuid4())


def check_auth_token(auth_token: str):
    if auth_token == '':
        raise KeyError('Auth token is empty!')
    if auth_token not in auth_dict:
        raise KeyError('Auth token token not valid!')


def auth_required(func):
    @functools.wraps(func)
    def wrapper(auth_token: str, **kwargs):
        check_auth_token(auth_token)
        return func(user=auth_dict[auth_token], **kwargs)
    return wrapper


def auth_not_required(func):
    @functools.wraps(func)
    def wrapper(auth_token: str, **kwargs):
        _ = auth_token
        return func(**kwargs)
    return wrapper


def admin_required(func):
    @functools.wraps(func)
    def wrapper(auth_token: str, **kwargs):
        check_auth_token(auth_token)
        user = auth_dict[auth_token]
        if not user.is_admin:
            raise PermissionError('Admin rights required!')
        return func(user=user, **kwargs)
    return wrapper
