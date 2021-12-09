from dns_exchange.helpers import Response
from dns_exchange.validators import Number


# mine command

class MineCommandData:
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        assert 'number' in kwargs.keys(), 'command "mine" requires argument "number"'
        self.number = kwargs['number']


def mine(**kwargs):
    data = MineCommandData(**kwargs)

    # TODO: mine_command logic

    return Response()
