from dns_exchange.handlers.helpers import auth_not_required
from dns_exchange.helpers import Response
from dns_exchange.models.mongo.transactions import Transaction
from dns_exchange.validators import Number


# list_transactions command
class ListTransactionsCommandData:
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        # Optional arguments
        self.number = kwargs['number'] if 'number' in kwargs.keys() else None


@auth_not_required
def list_transactions(**kwargs):
    data = ListTransactionsCommandData(**kwargs)
    response = Response()

    try:
        transactions = Transaction.list()
        response.add_content_table(
            "Transaction history",
            ["date", "from", "to", "token", "amount"],
            sorted(
                [[str(t.date), t.from_, t.to, t.token, t.amount] for t in transactions],
                key=lambda x: x[0],
                reverse=True
            )[:data.number]
        )
    except TypeError:
        response.add_error("no transactions!")

    return response
