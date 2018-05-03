from abc import ABCMeta, abstractmethod

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

def test_option_constructors():
    assert Option.none().is_empty()
    assert not Option.just(7).is_empty()

def test_option_map():
    assert Option.none().map(lambda x: x * 2).is_empty()
    assert Option.just(7).map(lambda x: x * 2).value == 14

def test_option_flatmap():
    assert Option.none().flatmap(lambda x: Option.just(x * 2)).is_empty()
    assert Option.just(7).flatmap(lambda x: Option.just(x * 7)).value == 49
    assert Option.just(7).flatmap(lambda x: Option.none()).is_empty()

def test_option_filter():
    assert Option.none().filter(lambda _: True).is_empty()
    assert not Option.just(7).filter(lambda _: True).is_empty()
    assert Option.just(7).filter(lambda _: False).is_empty()
    assert Option.just(7).filter(lambda x: x % 2 == 0).is_empty()

def test_list_constructors():
    assert List.empty().is_empty()
    assert not List.of(1, 2, 3).is_empty()

def test_list_map():
    assert List.empty().map(lambda x: x * 2).is_empty()
    assert not List.of(1, 2, 3).map(lambda x: x * 2).is_empty()

    assert_list_contains(
        List.of(1, 2, 3).map(lambda x: x * 2),
        (2, 4, 6)
    )

def assert_list_contains(lst, elements):

    tail = lst

    for element in elements:
        assert not tail.is_empty(), 'unexpected end of list'
        assert tail.head == element
        head, tail = tail.head, tail.tail

    assert tail.is_empty(), 'end of list was expected'

def test_assert_list_contains():
    assert_list_contains(List.empty(), ())
    assert_list_contains(List.of(1, 2, 3), (1, 2, 3))

def test_list_flatmap():
    assert_list_contains(
        List.of(1, 2).flatmap(
            lambda x: List.of(x, -x)
        ),
        (1, -1, 2, -2)
    )

def test_list_filter():
    assert_list_contains(
        List.of(2, 3, 4, 5, 6, 7, 8, 9).filter(
            lambda x: x % 2 + x % 3 == 1
        ),
        (3, 4, 9)
    )
