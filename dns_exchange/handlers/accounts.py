from dns_exchange.helpers import Response
from dns_exchange.services.Account import Account
from dns_exchange.validators import String, Number


# create_account command


def create_account():

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

    def __init__(self, **kwargs):
        assert 'seed_phrase' in kwargs.keys(), 'command "import_account" requires argument "seed_phrase"'
        self.seed_phrase = kwargs['seed_phrase']


def import_account(**kwargs):
    data = ImportAccountCommandData(**kwargs)

    # TODO: Import account logic

    return Response()


# my_account command


def my_account(**kwargs):

    # TODO: My account logic

    return Response()


# account_info command


class AccountsInfoCommandData:
    address = String(pattern=r'0x([a-f0-9]{8})')
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        assert 'address' in kwargs.keys(), 'command "account_info" requires argument "address"'
        self.address = kwargs['address']

        if 'number' in kwargs.keys():
            self.number = kwargs['number']


def account_info(**kwargs):
    data = AccountsInfoCommandData(**kwargs)

    # TODO: Account info logic

    return Response()
