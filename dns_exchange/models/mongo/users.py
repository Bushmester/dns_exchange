from dns_exchange.models.interfaces.users import UserAssetsInterface, UserInterface
from dns_exchange.models.mongo.common import BaseModelDictField as MongoBaseModelDictField, BaseModel as MongoBaseModel


class UserAssets(MongoBaseModelDictField, UserAssetsInterface):
    pass


class User(MongoBaseModel, UserInterface):
    complex_attrs = {'assets': UserAssets}
