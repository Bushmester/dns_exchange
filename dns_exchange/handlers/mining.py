from random import uniform, randrange

from dns_exchange.dictionaries import auth_dict
from dns_exchange.helpers import Response
from dns_exchange.validators import Number


TOKEN = uniform(0, 1000)
NUMBER = randrange(0, 10)


# mine command
class MineCommandData:
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        assert 'number' in kwargs.keys(), 'command "mine" requires argument "number"'
        self.number = kwargs['number']


def mine(auth_token: str, **kwargs):
    data = MineCommandData(**kwargs)
    # TODO: Mine logic
    response = Response()

    try:
        user = auth_dict[auth_token]

        if data.number == NUMBER:
            response.add_content_text(
                lines=[f"You've received {TOKEN} DNS tokens!"],
            )
        else:
            response.add_content_text(
                lines=["Unsuccessful mining!"],
            )
    except KeyError:
        response.add_error("auth is required!")

    return response
