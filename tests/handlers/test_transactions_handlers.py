import pytest

from dns_exchange.handlers import transactions
from dns_exchange.models.mongo.transactions import Transaction


@pytest.mark.usefixtures("clean_db")
def test_list_transactions():
    transactions_for_test = [['0x12c942a9', '0xe8e46109', 'STS', 228.228],
                             ['0xe8e46109', '0x12c942a9', 'TNT', 1337.1337]]

    number = len(transactions_for_test)

    for transaction in transactions_for_test[::-1]:
        Transaction.create(from_=transaction[0], to=transaction[1],
                           token=transaction[2], amount=transaction[3]).save()

    response_from_list_transactions = transactions.list_transactions(auth_token='', number=number)
    transactions_from_response = response_from_list_transactions.content[0]['rows']
    list(map(lambda x: x.pop(0), transactions_from_response))  # delete date

    assert str(transactions_from_response) == str(transactions_for_test)
