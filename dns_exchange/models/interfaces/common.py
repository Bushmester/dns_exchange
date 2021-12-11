from abc import ABC, abstractmethod
from typing import Any
from bson.objectid import ObjectId


class BaseDescriptorInterface(ABC):
    field_name = ''  # Must be specified by DescriptorInterface (e.g. "assets" for UserAssetsInterface)

    """Interface to work with"""

    def __init__(self, owner_id):
        self.owner_id = owner_id

    def __setitem__(self, key, value):
        self._set_value(key, value)

    def __getitem__(self, key):
        return self._get_value(key)

    def __delitem__(self, key):
        self._delete_value(key)

    """Methods that make interface work"""

    @abstractmethod
    def _set_value(self, key: str, value: Any):
        pass

    @abstractmethod
    def _get_value(self, key: str):
        pass

    @abstractmethod
    def _delete_value(self, key: str):
        pass


class BaseModelInterface(ABC):
    # Attributes below must be specified by ModelInterface
    table_name = ''
    _predefined_attrs = ('id',)
    __slots__ = (*_predefined_attrs,)

    """Interface to work with"""

    def __init__(self, **kwargs):
        self.id = ObjectId()

        self._create_obj(**kwargs)

    def __setattr__(self, key, value):
        if key in self._predefined_attrs:
            super().__setattr__(key, value)
        else:
            self._set_obj_attr(key, value)

    def __getattr__(self, key):
        if key in self._predefined_attrs:
            return super.__getattribute__(self, key)
        else:
            self._get_obj_attr(key)

    def __delattr__(self, key):
        if key in self._predefined_attrs:
            return super.__delattr__(self, key)
        else:
            self._del_obj_attr(key)

    @classmethod
    def retrieve(cls, **kwargs):
        return cls._retrieve_obj(**kwargs)

    # List method
    @classmethod
    def list(cls, **kwargs):
        return cls._list_objs(**kwargs)

    # Delete method
    def __del__(self):
        self._delete_obj()

    """Methods that make interface work"""

    @abstractmethod
    def _create_obj(self, **kwargs):
        pass

    @abstractmethod
    def _set_obj_attr(self, key: str, value: Any):
        pass

    @abstractmethod
    def _get_obj_attr(self, key: str):
        pass

    @abstractmethod
    def _del_obj_attr(self, key: str):
        pass

    @classmethod
    def _retrieve_obj(cls, **kwargs):
        pass

    @classmethod
    def _list_objs(cls, **kwargs):
        pass

    def _delete_obj(self):
        pass
