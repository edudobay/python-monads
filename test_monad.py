from monad import Option, List

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

# ---

def test_list_constructors():
    assert List.empty().is_empty()
    assert not List.of(1, 2, 3).is_empty()

def test_list_map():
    assert List.empty().map(lambda x: x * 2).is_empty()
    assert not List.of(1, 2, 3).map(lambda x: x * 2).is_empty()

    assert_list_matches(
        List.of(1, 2, 3).map(lambda x: x * 2),
        (2, 4, 6)
    )

def test_list_flatmap():
    assert_list_matches(
        List.of(1, 2).flatmap(
            lambda x: List.of(x, -x)
        ),
        (1, -1, 2, -2)
    )

def test_list_filter():
    assert_list_matches(
        List.of(2, 3, 4, 5, 6, 7, 8, 9).filter(
            lambda x: x % 2 + x % 3 == 1
        ),
        (3, 4, 9)
    )

# ---

def assert_list_matches(lst, elements):
    tail = lst

    for element in elements:
        assert not tail.is_empty(), 'unexpected end of list'
        assert tail.head == element
        head, tail = tail.head, tail.tail

    assert tail.is_empty(), 'end of list was expected'

def test_assert_list_matches():
    assert_list_matches(List.empty(), ())
    assert_list_matches(List.of(1, 2, 3), (1, 2, 3))

