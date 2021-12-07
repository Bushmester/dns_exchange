from dns_exchange.helpers import Response
from dns_exchange.services.Account import Account
from dns_exchange.validators import String


# create_account command


class CreateAccountCommandData:
    def __init__(self, *args):
        assert len(args) == 0, '"create_account" command doesn\'t take arguments'


def create_account():
    CreateAccountCommandData()

    new_account = Account()

    response = Response()
    response.add_content_text(
        title="New account has been successfully created!",
        lines=[
            f"address: {new_account.address}",
            f"seed_phrase: {new_account.seed_phrase}"
        ]
    )
    return response


# import_account command


class ImportAccountCommandData:
    seed_phrase = String(predicate=lambda x: len(x.split()) >= 6)

    def __init__(self, *args):
        assert len(args) == 1, '"import_account" command takes exactly 1 argument'
        self.seed_phrase = args[0]


def import_account(*args):
    data = ImportAccountCommandData(*args)

    # TODO: Import account logic

    return Response()
