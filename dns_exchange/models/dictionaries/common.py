from abc import abstractmethod, ABC


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
