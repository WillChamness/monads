from typing import Callable, TypeVar, Any, Generic, Union
from monad import then
from functor import wrapper

T = TypeVar("T")
U = TypeVar("U")

def maybe(wrapped: Callable[[Any], T|None], f: Callable[[T], Callable[[Any], U|None]]) -> Callable[[Any], U|None]:
    x: T|None = wrapped(None)

    if x is None:
        return wrapper(None)
    else:
        # wrapper(x) to satisfy mypy type checking
        return then(wrapper(x), f)



if __name__ == "__main__":
    def succ_of(n: int) -> Callable[[Any], int|None]:
        if n <= 0:
            return wrapper(None)
        else:
            return wrapper(n-1)

    def to_float(n: int) -> Callable[[Any], float|None]:
        if n == 1:
            return wrapper(None) 
        else:
            return wrapper(float(n))

    def inverse(x: float) -> Callable[[Any], str|None]: 
        if x == 0:
            return wrapper(None) 
        else:
            return wrapper(f"{1 / x:.3f}")


    n1: Callable[[Any], int] = wrapper(5)
    s1: str|None = maybe(
        maybe(
            maybe(
                n1,
                succ_of
            ),
            to_float
        ),
        inverse
    )(None)

    print(s1)
    assert s1 is not None
    assert isinstance(s1, str)
    assert s1 == f"{1 / (5 - 1):.3f}"

    n2: Callable[[Any], int] = wrapper(0)
    s2: str|None = maybe(
        maybe(
            maybe(
                n2,
                succ_of
            ),
            to_float
        ),
        inverse
    )(None)

    assert s2 is None

    n3: Callable[[Any], int] = wrapper(2)
    s3: str|None = maybe(
        maybe(
            maybe(
                n3,
                succ_of
            ),
            to_float
        ),
        inverse
    )(None)

    assert s3 is None

    n4: Callable[[Any], int] = wrapper(1)
    s4: str|None = maybe(
        maybe(
            maybe(
                n4,
                succ_of
            ),
            to_float
        ),
        inverse
    )(None)

    assert s4 is None
