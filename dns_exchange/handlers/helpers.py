import functools
import logging

from dns_exchange.dictionaries import auth_dict
from dns_exchange.helpers import Response
from dns_exchange.models.mongo.users import User


def check_auth_token(auth_token: str) -> None:
    if auth_token == '':
        raise KeyError('Auth token is empty!')
    if auth_token not in auth_dict:
        raise KeyError('Auth token token is not valid!')


def auth_required(func):
    @functools.wraps(func)
    def wrapper(auth_token: str, *args, **kwargs):
        check_auth_token(auth_token)
        return func(user=User.retrieve(id=auth_dict[auth_token]), *args, **kwargs)
    return wrapper


def auth_not_required(func):
    @functools.wraps(func)
    def wrapper(auth_token: str, *args, **kwargs):
        _ = auth_token
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    @functools.wraps(func)
    def wrapper(auth_token: str, *args, **kwargs):
        check_auth_token(auth_token)
        user = User.retrieve(id=auth_dict[auth_token])
        if not user.is_admin:
            raise PermissionError('Admin rights are required!')
        return func(*args, user=user, **kwargs)
    return wrapper


def catch_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(str(e))
            return Response(errors=['Server error occurred!'])
    return wrapper
