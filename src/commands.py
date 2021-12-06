import functools

from dictionaries import shared_dict, commands_dict
from validators import String


def register_command(func):
    commands_dict[func.__name__] = func
    return func


class GetCommandData:
    dict_key = String(minsize=3, maxsize=20)

    def __init__(self, *args):
        assert len(args) == 1, 'Get command takes exactly 1 argument'
        self.dict_key = args[0]


@register_command
def get_value(*args):
    get_data = GetCommandData(*args)
    return shared_dict.get(get_data.dict_key, f'No value with key {get_data.dict_key}')


class SetCommandData:
    dict_key = String(minsize=3, maxsize=20)
    dict_new_value = String(minsize=3, maxsize=100)

    def __init__(self, *args):
        assert len(args) == 2, 'Get command takes exactly 2 arguments'
        self.dict_key = args[0]
        self.dict_new_value = args[1]


@register_command
def set_value(*args):
    set_data = SetCommandData(*args)
    shared_dict[set_data.dict_key] = set_data.dict_new_value
    return f'Successfully saved {set_data.dict_key}={set_data.dict_new_value}'


@register_command
def bye(*args):
    raise StopIteration('User entered bye command')
