from typing import Callable

from dns_exchange.dictionaries import commands_dict
from dns_exchange.handlers.accounts import create_account


def register_command(func: Callable) -> Callable:
    commands_dict[func.__name__] = func
    return func


def register_all_commands():
    register_command(create_account)
