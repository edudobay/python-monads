from abc import ABCMeta, abstractmethod

__all__ = ['Monad']

class Monad(metaclass=ABCMeta):
    @abstractmethod
    def flatmap(self, mapper):
        return NotImplemented

    @classmethod
    @abstractmethod
    def unit(self):
        return NotImplemented

    def map(self, mapper):
        return self.flatmap(lambda v: self.unit(mapper(v)))

    def filter(self, predicate):
        return self.flatmap(lambda v: self.unit(v) if predicate(v) else self.zero())
