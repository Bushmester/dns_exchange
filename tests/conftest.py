import pytest

from dns_exchange.models.mongo.users import User
from dns_exchange.handlers import accounts
from dns_exchange.models.mongo.token_pairs import TokenPair, BuyOrder, SellOrder
from dns_exchange.models.mongo.transactions import Transaction


@pytest.fixture(scope='function')
def clean_db():
    models_for_clean = [TokenPair, BuyOrder, SellOrder, Transaction, User]

    for i in range(2):
        for model in models_for_clean:
            lst_with_objects = model.list()

            for obj in lst_with_objects:
                obj.delete()
        if i == 0:
            yield
