from .monad import Monad

__all__ = ['List']

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


