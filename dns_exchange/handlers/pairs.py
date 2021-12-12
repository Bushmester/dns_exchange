import re

from dns_exchange.handlers.helpers import admin_required, auth_not_required
from dns_exchange.helpers import Response
from dns_exchange.models.mongo.token_pairs import TokenPair
from dns_exchange.validators import String, IntNumber


# add_pair command
class AddPairCommandData:
    token1 = String(minsize=3, maxsize=4)
    token2 = String(minsize=3, maxsize=4)

    def __init__(self, **kwargs):
        # Required arguments
        assert 'token1' in kwargs.keys(), 'command "add_pair" requires argument "token1"'
        self.token1 = kwargs['token1']

        assert 'token2' in kwargs.keys(), 'command "add_pair" requires argument "token2"'
        self.token2 = kwargs['token2']


@admin_required
def add_pair(user, **kwargs):
    _ = user
    data = AddPairCommandData(**kwargs)
    response = Response()

    token_pair = None

    try:
        token_pair = TokenPair.retrieve(label=f'{data.token1}_{data.token2}')
    except TypeError:
        pass

    try:
        token_pair = TokenPair.retrieve(label=f'{data.token2}_{data.token1}')
    except TypeError:
        pass

    if token_pair is not None:
        response.add_error("Pair already exists!")
    else:
        TokenPair.create(label=f'{data.token1}_{data.token2}').save()
        response.add_content_text(title=f'{data.token1}_{data.token2} pair has been successfully added!')

    return response


# delete_pair command
class DeletePairCommandData:
    label = String(pattern=r'[A-Z]{3,4}_[A-Z]{3,4}')

    def __init__(self, **kwargs):
        # Required arguments
        assert 'label' in kwargs.keys(), 'command "delete_pair" requires argument "label"'
        self.label = kwargs['label']


@admin_required
def delete_pair(user, **kwargs):
    _ = user
    data = DeletePairCommandData(**kwargs)
    response = Response()

    try:
        token_pair = TokenPair.retrieve(label=data.label)
    except TypeError:
        response.add_error("Pair label is incorrect!")
    else:
        token_pair.delete()
        response.add_content_text(title=f"{data.label} pair has been successfully removed!")

    return response


# list_pairs command
class ListPairsCommandData:
    filter_by_label = String()

    def __init__(self, **kwargs):
        # Optional arguments
        self.filter_by_label = kwargs['filter_by_label'] if 'filter_by_label' in kwargs.keys() else None


@auth_not_required
def list_pair(**kwargs):
    data = ListPairsCommandData(**kwargs)
    response = Response()

    pattern = r'([A-Z]{3,4}_' + f'{data.filter_by_label})' + r'|' + f'({data.filter_by_label}_' + r'[A-Z]{3,4})'
    token_pairs_filtered = list(filter(lambda x: re.fullmatch(pattern, x.label), TokenPair.list()))

    if token_pairs_filtered:
        response.add_content_table("", ["label"], [tp.label for tp in token_pairs_filtered])
    else:
        response.add_content_text(title="No pairs found!")

    return response


# pair_info command
class PairInfoCommandData:
    label = String(pattern=r'[A-Z]{3,4}_[A-Z]{3,4}')
    number = IntNumber(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        # Required arguments
        assert 'label' in kwargs.keys(), 'command "pair_info" requires argument "label"'
        self.label = kwargs['label']

        # Optional arguments
        self.number = kwargs['number'] if 'number' in kwargs.keys() else None


@auth_not_required
def pair_info(**kwargs):
    data = PairInfoCommandData(**kwargs)
    # TODO: Pair info logic
    return Response()
