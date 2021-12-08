from dns_exchange.helpers import Response
from dns_exchange.validators import String, Number


# add_pair command

class AddPairCommandData:
    token1 = String(minsize=3, maxsize=4)
    token2 = String(minsize=3, maxsize=4)

    def __init__(self, **kwargs):
        assert len(kwargs) == 2, '"add_pair" command takes exactly 2 arguments'
        self.token1 = kwargs['token1']
        self.token2 = kwargs['token2']


def add_pair(**kwargs):
    data = AddPairCommandData(**kwargs)

    # TODO: Add pair logic

    return Response()


# delete_pair command


class DeletePairCommandData:
    pair_pattern = r'[a-z]{3,4}_[a-z]{3,4}'

    label = String(pattern=pair_pattern)

    def __init__(self, **kwargs):
        assert len(kwargs) == 1, '"delete_pair" command takes exactly 1 argument'
        self.label = kwargs['label']


def delete_pair(**kwargs):
    data = DeletePairCommandData(**kwargs)

    # TODO: Delete pair logic

    return Response()


# list_pairs command


class ListPairsCommandData:
    filter_by_label = String()

    def __init__(self, **kwargs):
        assert len(kwargs) < 2, '"list_pairs" takes maximum 1 argument'

        if len(kwargs) == 1:
            self.filter_by_label = kwargs['filter_by_label']


def list_pair(**kwargs):
    data = ListPairsCommandData(**kwargs)

    # TODO: List pairs logic

    return Response()


# pair_info command

class PairInfoCommandData:
    pair_pattern = r'[a-z]{3,4}_[a-z]{3,4}'

    label = String(pattern=pair_pattern)
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        assert len(kwargs) != 0 and len(kwargs) <= 2, '"pair_info" command takes minimum 1 and maximum 2 arguments'
        self.label = kwargs['label']

        if len(kwargs) == 2:
            self.number = kwargs['number']


def pair_info(**kwargs):
    data = PairInfoCommandData(**kwargs)

    # TODO: Pair info logicF

    return Response()
