from uuid import uuid4

from dns_exchange.helpers import Response
from dns_exchange.models.mongo.transactions import Transaction
from dns_exchange.models.mongo.users import User
from dns_exchange.validators import String, Number
from dns_exchange.dictionaries import auth_dict


def generate_auth_token():
    return uuid4()


# create_account command
def create_account():
    new_account = User.create()
    response = Response()
    response.add_content_text(
        title="New account has been successfully created!",
        lines=[f"address: {new_account.address}", f"seed_phrase: {new_account.seed_phrase}"],
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
    response = Response()

    try:
        user = User.retrieve(seed_phrase=data.seed_phrase)
        auth_token = str(generate_auth_token())
        auth_dict[auth_token] = user

        response.auth_token = auth_token
        response.add_content_text(
            lines=["Account has been successfully imported!"],
        )
    except TypeError:
        response.add_error("seed phrase is incorrect!")

    return response


# my_account command
def my_account(auth_token: str, **kwargs):
    response = Response()

    try:
        user = auth_dict[auth_token]

        response.add_content_text(
            lines=[f"address: {user.address}"],
        )
    except KeyError:
        response.add_error("auth is required!")

    return response


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
    response = Response()

    try:  # TODO: Any ideas on how to make it clean?
        user = User.retrieve(address=data.address)
        response.add_content_table(
            "ASSETS",
            ["token", "amount"],
            [[key, val] for key, val in user.assets][:data.number]  # TODO: How to slice without copy?
        )

        try:
            user_transactions = Transaction.list(from_=user.address)
            response.add_content_table(
                "TRANSACTION HISTORY",
                ["date", "from", "to", "token", "amount"],
                [[str(t.date), t.from_, t.to, t.token, t.amount] for t in user_transactions][:data.number]  # TODO: Any ideas on how to make it clean?
            )
        except TypeError:
            pass

    except TypeError:
        response.add_error("address in incorrect!")

    # TODO: Account info logic
    return response
