from dns_exchange.dictionaries import auth_dict
from dns_exchange.helpers import Response
from dns_exchange.validators import Number
from dns_exchange.handlers.helpers import get_random_mine_number, get_random_token_amount


# mine command
class MineCommandData:
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        assert 'number' in kwargs.keys(), 'Command "mine" requires argument "number"'
        self.number = kwargs['number']


def mine(auth_token: str, **kwargs):
    data = MineCommandData(**kwargs)
    response = Response()

    try:
        if data.number == get_random_mine_number():
            token_amount = get_random_token_amount()
            user = auth_dict[auth_token]
            user.assets['DNS'] = user.assets['DNS'] + token_amount if 'DNS' in dict(user.assets) else token_amount
            response.add_content_text(title=f"You've received {token_amount} DNS tokens!")
        else:
            response.add_content_text(title="Unsuccessful mining!")

    except KeyError:
        response.add_error('Auth is required!')

    return response
