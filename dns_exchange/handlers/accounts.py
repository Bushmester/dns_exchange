from dns_exchange.helpers import Response
from dns_exchange.services.Account import Account
from dns_exchange.validators import String, Number, Address, Pair


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


# my_account command


class MyAccountCommandData:
    def __init__(self, *args):
        assert len(args) == 0


def my_account(*args):
    data = MyAccountCommandData(*args), '"my_account" command doesn\'t take arguments'

    # TODO: Import my_account

    return Response()


# account_info command


class AccountsInfoCommandData:
    address = Address()
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, *args):
        assert len(args) != 0 and len(args) <= 2, '"account_info" command takes minimum 1 and maximum 2 arguments'
        self.address = args[0]

        if len(args) > 1:
            self.number = args[1]


def account_info(*args):
    data = AccountsInfoCommandData(*args)

    # TODO: Account info logic

    return Response()


# add_token command


class AddTokenCommandData:
    tag = String(minsize=3, maxsize=4)
    quantity = Number(minvalue=0)

    def __init__(self, *args):
        assert len(args) == 2, '"add_token" command takes exactly 2 argument'
        self.tag = args[0]
        self.quantity = args[1]


def add_token(*args):
    data = AccountsInfoCommandData(*args)

    # TODO: Add token logic

    return Response()


# buy command


class BuyCommandData:
    trading_pair = String(minsize=3, maxsize=4)
    amount = Number(minvalue=0)
    exchange_rate = Number(minvalue=0)

    def __init__(self, *args):
        assert len(args) == 2, '"buy" command takes exactly 2 argument'
        self.trading_pair = args[0]
        self.amount = args[1]

        if len(args) > 2:
            self.exchange_rate = args[2]


def buy(*args):
    data = AccountsInfoCommandData(*args)

    # TODO: Buy logic

    return Response()


# sell command


class SellCommandData:
    trading_pair = String(minsize=3, maxsize=4)
    amount = Number(minvalue=0)
    exchange_rate = Number(minvalue=0)

    def __init__(self, *args):
        assert len(args) == 2, '"sell" command takes exactly 2 argument'
        self.trading_pair = args[0]
        self.amount = args[1]

        if len(args) > 2:
            self.exchange_rate = args[2]


def sell(*args):
    data = AccountsInfoCommandData(*args)

    # TODO: Sell logic

    return Response()


# add_pair command

class AddPairCommandData:
    token1 = String(minsize=3, maxsize=4)
    token2 = String(minsize=3, maxsize=4)

    def __init__(self, *args):
        assert len(args) == 2, '"add_pair" command takes exactly 2 argument'
        self.token1 = args[0]
        self.token2 = args[1]


def add_pair(*args):
    data = AddPairCommandData(*args)

    # TODO: Add pair logic

    return Response()


# delete_pair command


class DeletePairCommandData:
    label = Pair()

    def __init__(self, *args):
        assert len(args) == 1, '"delete_pair" command takes exactly 1 argument'
        self.label = args[0]


def delete_pair(*args):
    data = AddPairCommandData(*args)

    # TODO: Delete pair logic

    return Response()


# list_pairs command


class ListPairsCommandData:
    filter_by_label = String()

    def __init__(self, *args):
        assert len(args) < 2, '"list_pairs" takes maximum 1 argument'

        if len(args) == 1:
            self.filter_by_label = args[0]


def list_pair(*args):
    data = ListPairsCommandData(*args)

    # TODO: List pairs logic

    return Response()


# pair_info command

class PairInfoCommandData:
    label = Pair()
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, *args):
        assert len(args) != 0 and len(args) <= 2, '"pair_info" command takes minimum 1 and maximum 2 arguments'
        self.label = args[0]

        if len(args) == 2:
            self.number = args[1]


def pair_info(*args):
    data = PairInfoCommandData(*args)

    # TODO: Pair info logic

    return Response()


# list_transactions command


class ListTransactionsCommandData:
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, *args):
        assert len(args) == 0 and len(args) <= 1, '"list_transactions" command takes minimum 0 and maximum 1 arguments'
        if len(args) == 1:
            self.number = args[0]


def list_transactions(*args):
    data = ListTransactionsCommandData(*args)

    # TODO: list_pair logic

    return Response()


# mine command

class MineCommandData:
    number = Number(minvalue=1, maxvalue=50)

    def __init__(self, *args):
        assert len(args) == 1, '"mine_command" command takes exactly 1 argument'
        number = args[0]


def mine(*args):
    data = MineCommandData(*args)

    # TODO: mine_command logic

    return Response()







