from dictionaries import commands_dict


def register_command(func):
    commands_dict[func.__name__] = func
    return func


