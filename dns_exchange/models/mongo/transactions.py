from dns_exchange.models.interfaces.transactions import TransactionInterface
from dns_exchange.models.mongo.common import MongoBaseModel


class Transaction(MongoBaseModel, TransactionInterface):
    pass
