from random import uniform, randrange
from uuid import uuid4


def get_random_mine_number():
    return randrange(0, 10)


def get_random_token_amount():
    return uniform(0, 10)


def generate_auth_token():
    return str(uuid4())
