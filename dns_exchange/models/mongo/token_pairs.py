from dns_exchange.models.interfaces.token_pairs import BuyOrderInterface, SellOrderInterface, TokenPairInterface
from dns_exchange.models.mongo.common import BaseModel as MongoBaseModel


class BuyOrder(MongoBaseModel, BuyOrderInterface):
    pass


class SellOrder(MongoBaseModel, SellOrderInterface):
    pass


class TokenPair(MongoBaseModel, TokenPairInterface):
    pass
