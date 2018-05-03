from abc import abstractmethod
from .monad import Monad

__all__ = ['Option']

class Option(Monad):
    @abstractmethod
    def is_empty(self):
        return NotImplemented

    @classmethod
    def just(cls, value):
        return _Option_Just(value)

    @classmethod
    def none(cls):
        return _Option_None.instance()

    @classmethod
    def unit(cls, value):
        return cls.just(value)

    @classmethod
    def zero(cls):
        return cls.none()

class _Option_Just(Option):
    def __init__(self, value):
        self.value = value

    def flatmap(self, mapper):
        return mapper(self.value)

    def is_empty(self):
        return False

class _Option_None(Option):
    _INSTANCE = None

    @classmethod
    def instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def flatmap(self, mapper):
        return Option.none()

    def is_empty(self):
        return True
