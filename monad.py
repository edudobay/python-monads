from abc import ABCMeta, abstractmethod

__all__ = ['Monad', 'Option', 'List']

class Monad(metaclass=ABCMeta):
    @abstractmethod
    def flatmap(self, mapper):
        return NotImplemented

    def map(self, mapper):
        return self.flatmap(lambda v: self.unit(mapper(v)))

    def filter(self, predicate):
        return self.flatmap(lambda v: self.unit(v) if predicate(v) else self.zero())

class List(Monad):

    @classmethod
    def empty(cls):
        return _List_Nil.instance()

    @classmethod
    def cons(cls, value, lst):
        return _List_Cons(value, lst)

    @classmethod
    def of(cls, *args):
        bot = List.empty()
        lst = bot
        for arg in reversed(args):
            lst = List.cons(arg, lst)
        return lst

    @classmethod
    def unit(cls, value):
        return cls.of(value)

    @classmethod
    def zero(cls):
        return cls.empty()

    def is_empty(self):
        return not bool(self.values)

    @classmethod
    def concat(cls, lst1, lst2):
        if not lst1.is_empty():
            return List.cons(lst1.head, cls.concat(lst1.tail, lst2))
        else:
            return lst2

class _List_Nil(List):
    _INSTANCE = None

    @classmethod
    def instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def is_empty(self):
        return True

    def flatmap(self, mapper):
        return _List_Nil.instance()

class _List_Cons(List):
    def __init__(self, value, lst):
        self.head = value
        self.tail = lst

    def is_empty(self):
        return False

    def flatmap(self, mapper):
        v = mapper(self.head)
        tail = self.tail.flatmap(mapper)
        return List.concat(v, tail)

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
