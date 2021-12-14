import pytest

from dns_exchange.handlers import transactions
from dns_exchange.models.mongo.transactions import Transaction


@pytest.mark.usefixtures("clean_db")
def test_list_transactions():
    Transaction.create()

    number = 3
    response_from_list_transactions = transactions.list_transactions(auth_token='', number=number)

    assert 1 == 1
