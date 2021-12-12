from dns_exchange.handlers.helpers import auth_not_required, auth_required, generate_auth_token
from dns_exchange.helpers import Response
from dns_exchange.models.mongo.transactions import Transaction
from dns_exchange.models.mongo.users import User
from dns_exchange.validators import String, IntNumber
from dns_exchange.dictionaries import auth_dict


# create_account command
@auth_not_required
def create_account():
    new_account = User.create().save()
    response = Response()
    response.add_content_text(
        title="New account has been successfully created!",
        lines=[
            f"address: {new_account.address}",
            f"seed_phrase: {new_account.seed_phrase}"
        ],
    )
    return response


# import_account command
class ImportAccountCommandData:
    seed_phrase = String(predicate=lambda x: len(x.split()) >= 6)

    def __init__(self, **kwargs):
        # Required arguments
        assert 'seed_phrase' in kwargs.keys(), 'Command "import_account" requires argument "seed_phrase"'
        self.seed_phrase = kwargs['seed_phrase']


@auth_not_required
def import_account(**kwargs):
    data = ImportAccountCommandData(**kwargs)
    response = Response()

    try:
        user = User.retrieve(seed_phrase=data.seed_phrase)
    except TypeError:
        response.add_error("Seed phrase is incorrect!")
    else:
        auth_token = generate_auth_token()
        auth_dict[auth_token] = user
        response.auth_token = auth_token
        response.add_content_text(title="Account has been successfully imported!")

    return response


# my_account command
@auth_required
def my_account(user):
    response = Response()
    response.add_content_text(lines=[f"address: {user.address}"])
    return response


# account_info command
class AccountsInfoCommandData:
    address = String(pattern=r'0x([a-f0-9]{8})')
    number = IntNumber(minvalue=1, maxvalue=50)

    def __init__(self, **kwargs):
        # Required arguments
        assert 'address' in kwargs.keys(), 'Command "account_info" requires argument "address"'
        self.address = kwargs['address']

        # Required arguments
        self.number = kwargs['number'] if 'number' in kwargs else None


@auth_not_required
def account_info(**kwargs):
    data = AccountsInfoCommandData(**kwargs)
    response = Response()

    try:
        user = User.retrieve(address=data.address)
    except TypeError:
        response.add_error("Address in incorrect!")
    else:
        response.add_content_table("Assets", ["token", "amount"], list(dict(user.assets).items()))
        user_transactions = Transaction.list(from_=user.address)
        response.add_content_table(
            "Transactions history",
            ["date", "from", "to", "token", "amount"],
            sorted(
                [[str(ut.date), ut.from_, ut.to, ut.token, ut.amount] for ut in user_transactions],
                key=lambda x: x[0],
                reverse=True
            )[:data.number]
        )

    return response
