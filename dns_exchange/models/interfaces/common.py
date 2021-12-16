from abc import abstractmethod, ABC
from typing import Any, List

from dns_exchange.models.interfaces.errors import ArgumentError
from dns_exchange.models.interfaces.helpers import get_id


class AuthDictionaryInterface(ABC):
    @abstractmethod
    def __contains__(self, item):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def __delitem__(self, key):
        pass


class DBTransactionInterface(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, tb):
        pass


class BaseModelDictFieldInterface(ABC):
    attr_name = ''  # Set attribute name here, e.g. 'assets'

    def __init__(self, owner_id, owner_model_name):
        self._owner_id = owner_id
        self._owner_model_name = owner_model_name
        self._values_to_save = {}

    """Methods"""

    def __setitem__(self, key, value):
        self._values_to_save[key] = value

    def __getitem__(self, key):
        return self._get_value(key)

    def __delitem__(self, key):
        self._delete_value(key)

    def __iter__(self):
        for key, val in self._list_values().items():
            yield key, val

    def save(self):
        if self._values_to_save:
            for key, val in self._values_to_save.items():
                self._set_value(key, val)
            self._values_to_save = {}

    """Abstract methods that make interface work"""

    @abstractmethod
    def _set_value(self, key: str, value: Any):
        pass

    @abstractmethod
    def _get_value(self, key: str):
        pass

    @abstractmethod
    def _delete_value(self, key: str):
        pass

    @abstractmethod
    def _list_values(self):
        pass


class BaseModelInterface(ABC):
    model_name = ''  # Set model name here, e.g. 'users'
    complex_attrs = {}  # Dict of complex attributes + their actual implemented class, e.g. {'assets': UserAssets}
    required_attrs = {}  # Dict of required attributes + their types, e.g. {'from': hex}
    optional_attrs = {}  # Dict of optional attributes + their types, e.g. {'is_admin': bool}

    def __init__(self, obj_id, is_new, **kwargs):
        self._id = obj_id
        self._is_new = is_new
        self._attrs_to_save = {**kwargs}

        for attr_name, attr_class in self.complex_attrs.items():
            setattr(self, f'_{attr_name}', attr_class(self._id, self.model_name))

        # Initialize complex attributes here
        # e.g. self._assets = UserAssets(self._id)

    @classmethod
    def get_default_kwargs(cls, **kwargs):
        return {
            # Set default attributes here, e.g. name: 'DefaultName'
            'id': get_id(),
            **kwargs
        }

    def save_complex_attrs(self):
        for attr_name in self.complex_attrs:
            getattr(self, f'_{attr_name}').save()

    """Interface to work with"""

    @classmethod
    def create(cls, **kwargs):
        if len(kwargs) < len(cls.required_attrs):
            raise ArgumentError(f'Expected {len(cls.required_attrs)} required arguments, but got {len(kwargs)}')
        if len(kwargs) > len(cls.required_attrs) + len(cls.optional_attrs):
            raise ArgumentError(
                f'Expected maximum {len(cls.required_attrs) + len(cls.optional_attrs)} arguments, but got {len(kwargs)}'
            )
        for key, key_type in cls.required_attrs.items():
            if key not in kwargs:
                raise ArgumentError(f'Missing required "{key}" argument')
            if not isinstance(kwargs[key], key_type):
                raise ArgumentError(f'Argument "{key}" must be of type "{key_type}"')
        for key, key_type in cls.optional_attrs.items():
            if key in kwargs:
                if not isinstance(kwargs[key], key_type):
                    raise ArgumentError(f'Argument "{key}" must be of type "{key_type}"')
        default_kwargs = cls.get_default_kwargs(**kwargs)
        return cls(**default_kwargs, obj_id=default_kwargs['id'], is_new=True)

    @classmethod
    def retrieve(cls, **kwargs):
        obj_id = kwargs['id'] if 'id' in kwargs.keys() else cls._retrieve_obj(**kwargs)['id']
        return cls(obj_id=obj_id, is_new=False)

    @classmethod
    def list(cls, **kwargs):
        return [cls.retrieve(id=obj_data['id']) for obj_data in cls._list_objs(**kwargs)]

    def __getattr__(self, key):
        if key in self.complex_attrs:
            return getattr(self, f'_{key}')
        return self._get_obj_attr(key)

    def __setattr__(self, key, value):
        if key in self.complex_attrs:
            raise AttributeError('You can\'t set this attribute explicitly')
        if key[0] == '_':
            super().__setattr__(key, value)
        else:
            self._attrs_to_save[key] = value

    def save(self):
        if self._attrs_to_save:
            if self._is_new:
                self._create_obj(**self._attrs_to_save)
                self._is_new = False
            else:
                self._update_obj(**self._attrs_to_save)
        self.save_complex_attrs()

    def delete(self):
        self._delete_obj()
        del self

    """Abstract methods that make interface work"""

    @classmethod
    @abstractmethod
    def _create_obj(cls, **kwargs):
        pass

    @abstractmethod
    def _update_obj(self, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def _retrieve_obj(cls, **kwargs) -> dict:
        pass

    @abstractmethod
    def _get_obj_attr(self, key) -> Any:
        pass

    @classmethod
    @abstractmethod
    def _list_objs(cls, **kwargs) -> List[dict]:
        pass

    @abstractmethod
    def _delete_obj(self):
        pass
