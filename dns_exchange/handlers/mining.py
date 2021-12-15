from random import uniform, randrange

from dns_exchange.handlers.helpers import auth_required, catch_errors
from dns_exchange.helpers import Response
from dns_exchange.validators import IntNumber


# Helpers
def get_random_mine_number() -> int:
    return randrange(1, 10)


def get_random_token_amount() -> float:
    return uniform(0, 10)


# mine command
class MineCommandData:
    number = IntNumber(minvalue=1, maxvalue=10)

    def __init__(self, **kwargs):
        # Required arguments
        assert 'number' in kwargs.keys(), 'Command "mine" requires argument "number"'
        self.number = kwargs['number']


@catch_errors
@auth_required
def mine(user, **kwargs):
    data = MineCommandData(**kwargs)
    response = Response()

    if data.number == get_random_mine_number():
        token_amount = get_random_token_amount()
        user_assets = dict(user.assets)
        user.assets['DNS'] = user_assets['DNS'] + token_amount if 'DNS' in user_assets else token_amount
        user.save()
        response.add_content_text(title=f"You've received {token_amount} DNS tokens!")
    else:
        response.add_content_text(title="Unsuccessful mining!")

    return response
