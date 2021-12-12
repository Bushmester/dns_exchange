from dns_exchange.helpers import Response
from dns_exchange.models.mongo.transactions import Transaction
from dns_exchange.validators import Number


# list_transactions command
class ListTransactionsCommandData:
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        if 'number' in kwargs.keys():
            self.number = kwargs['number']


def list_transactions(**kwargs):
    data = ListTransactionsCommandData(**kwargs)
    response = Response()

    try:
        transactions = Transaction.list()
        response.add_content_table(
            "TRANSACTION HISTORY",
            ["date", "from", "to", "token", "amount"],
            sorted(
                [[str(t.date), t.from_, t.to, t.token, t.amount] for t in transactions][:data.number],
                key=lambda trans: trans[0],
                reverse=True
            )  # TODO: Any ideas on how to make it clean?
        )
    except TypeError:
        response.add_error("no transactions!")

    return response
