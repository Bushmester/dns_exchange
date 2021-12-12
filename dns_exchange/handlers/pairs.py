from dns_exchange.helpers import Response
from dns_exchange.models.mongo.token_pairs import TokenPair
from dns_exchange.validators import String, Number


# add_pair command
class AddPairCommandData:
    token1 = String(minsize=3, maxsize=4)
    token2 = String(minsize=3, maxsize=4)

    def __init__(self, **kwargs):
        assert 'token1' in kwargs.keys(), 'command "add_pair" requires argument "token1"'
        self.token1 = kwargs['token1']

        assert 'token2' in kwargs.keys(), 'command "add_pair" requires argument "token2"'
        self.token2 = kwargs['token2']


def add_pair(**kwargs):
    data = AddPairCommandData(**kwargs)
    response = Response()

    try:
        TokenPair.retrieve(label=f'{data.token1}_{data.token2}')
    except TypeError:
        try:
            TokenPair.retrieve(label=f'{data.token2}_{data.token1}')
        except TypeError:
            TokenPair.create(label=f'{data.token1}_{data.token2}').save()

            response.add_content_text(title=f'{data.token1}_{data.token2} pair has been successfully added!')
        else:
            response.add_error("Pair already exsists!")
    else:
        response.add_error("Pair already exsists!")
    return response


# delete_pair command
class DeletePairCommandData:
    label = String(pattern=r'[a-z]{3,4}_[a-z]{3,4}')

    def __init__(self, **kwargs):
        assert 'label' in kwargs.keys(), 'command "delete_pair" requires argument "label"'
        self.label = kwargs['label']


def delete_pair(**kwargs):
    data = DeletePairCommandData(**kwargs)
    # TODO: Delete pair logic
    return Response()


# list_pairs command
class ListPairsCommandData:
    filter_by_label = String()

    def __init__(self, **kwargs):
        if 'filter_by_label' in kwargs.keys():
            self.filter_by_label = kwargs['filter_by_label']


def list_pair(**kwargs):
    data = ListPairsCommandData(**kwargs)
    # TODO: List pairs logic
    return Response()


# pair_info command
class PairInfoCommandData:
    label = String(pattern=r'[a-z]{3,4}_[a-z]{3,4}')
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        assert 'label' in kwargs.keys(), 'command "pair_info" requires argument "label"'
        self.label = kwargs['label']

        if 'number' in kwargs:
            self.number = kwargs['number']


def pair_info(**kwargs):
    data = PairInfoCommandData(**kwargs)
    # TODO: Pair info logic
    return Response()
