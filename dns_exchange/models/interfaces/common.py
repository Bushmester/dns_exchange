from abc import ABC, abstractmethod
from typing import Any


class BaseDescriptorInterface(ABC):
    field_name = ''  # Must be specified by DescriptorInterface (e.g. "assets" for UserAssetsInterface)

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


class BaseModelInterface(ABC):
    table_name = ''  # Must be specified by ModelInterface (e.g. "users" for UserInterface)
    __slots__ = ('id',)

    """Interface to work with"""

    # Create method
    def __init__(self, **kwargs):
        obj_id = self._generate_id()
        self._create_obj(id=obj_id, **kwargs)

        self.id = obj_id

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
