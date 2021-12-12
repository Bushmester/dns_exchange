from dns_exchange.models.interfaces.users import UserAssetsInterface, UserInterface
from dns_exchange.models.mongo.common import MongoBaseModelDictField, MongoBaseModel


class UserAssets(MongoBaseModelDictField, UserAssetsInterface):
    pass


class User(MongoBaseModel, UserInterface):
    @staticmethod
    def get_user_assets_class():
        return UserAssets