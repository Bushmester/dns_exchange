from typing import Callable

from dns_exchange.dictionaries import commands_dict
from dns_exchange.handlers.accounts import create_account, import_account, my_account, account_info
from dns_exchange.handlers.mining import mine
from dns_exchange.handlers.pairs import add_pair, delete_pair, pair_info, list_pairs
from dns_exchange.handlers.tokens import add_token, buy, sell
from dns_exchange.handlers.transactions import list_transactions


def register_command(func: Callable) -> Callable:
    commands_dict[func.__name__] = func
    return func


def register_all_commands():
    # Accounts
    register_command(create_account)
    register_command(import_account)
    register_command(my_account)
    register_command(account_info)

    # Tokens
    register_command(add_token)
    register_command(buy)
    register_command(sell)

    # Pairs
    register_command(add_pair)
    register_command(delete_pair)
    register_command(list_pairs)
    register_command(pair_info)

    # Transactions
    register_command(list_transactions)

    # Mining
    register_command(mine)
