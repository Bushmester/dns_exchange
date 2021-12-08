from dns_exchange.helpers import Response
from dns_exchange.services.Account import Account
from dns_exchange.validators import String, Number


# create_account command


class CreateAccountCommandData:
    def __init__(self, **kwargs):
        assert len(kwargs) == 0, '"create_account" command doesn\'t take arguments'


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

    def __init__(self, **kwargs):
        assert len(kwargs) == 1, '"import_account" command takes exactly 1 argument'
        self.seed_phrase = kwargs['seed_phrase']


def import_account(**kwargs):
    data = ImportAccountCommandData(**kwargs)

    # TODO: Import account logic

    return Response()


# my_account command®


class MyAccountCommandData:
    def __init__(self, **kwargs):
        assert len(kwargs) == 0


def my_account(**kwargs):
    data = MyAccountCommandData(**kwargs), '"my_account" command doesn\'t take arguments'

    # TODO: Import my_account

    return Response()


# account_info command


class AccountsInfoCommandData:
    address_pattern = r'0x([a-f0-9]{8})'

    address = String(pattern=address_pattern)
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        assert len(kwargs) in (1, 2), '"account_info" command takes minimum 1 and maximum 2 arguments'
        self.address = kwargs['address']

        if len(kwargs) == 2:
            self.number = kwargs['number']


def account_info(**kwargs):
    data = AccountsInfoCommandData(**kwargs)

    # TODO: Account info logic

    return Response()
