import requests

from random import randrange, sample
from bson import ObjectId

from dns_exchange.config import WORDS_LINK


words_sites = requests.get(WORDS_LINK)
words = words_sites.content.splitlines()


def get_user_address():
    return hex(randrange(0, 4294967295))


def get_user_seed_phrase():
    return ' '.join(x.decode('utf-8') for x in sample(words, 8))


def get_id():
    return str(ObjectId())
