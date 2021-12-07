from dns_exchange.handlers.test import echo
from dns_exchange.helpers import register_command


def register_all_commands():
    register_command(echo)
