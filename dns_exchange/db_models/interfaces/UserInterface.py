from abc import ABC, abstractmethod
from typing import Any


class UserAssetsInterface(ABC):
    field_name = 'assets'

    """Interface to work with"""

    def __set__(self, instance, value):
        self._set_value_by_user_id(instance.id, value)

    def __get__(self, instance, owner):
        return self._get_value_by_user_id(instance.id)

    """Methods that make interface work"""

    @staticmethod
    @abstractmethod
    def _set_value_by_user_id(user_id: int, value: Any):
        pass

    @staticmethod
    @abstractmethod
    def _get_value_by_user_id(user_id: int):
        pass


class UserInterface(ABC):
    table_name = 'users'
    __slots__ = ('id', 'address', 'seed_phrase', 'is_admin', 'assets')

    """Interface to work with"""

    # Create method
    def __init__(self):
        obj_id = self._generate_id()
        self._create_obj(id=obj_id, assets={})

        self.id = obj_id
        self.address = '0x9c3f7c50'  # TODO: Generate address
        self.seed_phrase = 'red blue green yellow orange dick'  # TODO: Generate seed_phrase
        self.is_admin = False
        self.__class__.assets = self._get_assets_descriptor_obj()

    # Update method
    def __setattr__(self, item, value):
        super().__setattr__(item, value)
        self._update_by_id(self.id, item, value)

    # Retrieve method
    @classmethod
    def retrieve(cls, **kwargs):
        return cls._retrieve_obj(**kwargs)

    # List method
    @classmethod
    def list(cls, **kwargs):
        return cls._list_obj(**kwargs)

    # Delete method
    def __del__(self):
        self._delete_by_id(self.id)

    """Methods that make interface work"""

    @staticmethod
    @abstractmethod
    def _generate_id():
        pass

    @staticmethod
    @abstractmethod
    def _get_assets_descriptor_obj():
        # Simply uncomment line below
        # return UserAssets()
        pass

    @staticmethod
    @abstractmethod
    def _create_obj(**kwargs):
        pass

    @staticmethod
    @abstractmethod
    def _retrieve_obj(**kwargs):
        pass

    @staticmethod
    @abstractmethod
    def _list_obj(**kwargs):
        pass

    @staticmethod
    @abstractmethod
    def _update_by_id(obj_id: int, field_name: str, new_value: Any):
        pass

    @staticmethod
    @abstractmethod
    def _delete_by_id(obj_id: int):
        pass
