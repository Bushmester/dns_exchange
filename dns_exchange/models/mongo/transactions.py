from dns_exchange.models.interfaces.transactions import TransactionInterface
from dns_exchange.models.mongo.common import BaseModel as MongoBaseModel


class Transaction(MongoBaseModel, TransactionInterface):
    pass
