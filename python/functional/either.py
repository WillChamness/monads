from typing import Callable, TypeVar, Any, Generic, Union
from monad import then
from functor import wrapper

T = TypeVar("T")
TSuccess = TypeVar("TSuccess")

def either(wrapped: Callable[[Any], Exception|T], f: Callable[[T], Callable[[Any], Exception|TSuccess]]) -> Callable[[Any], Exception|TSuccess]:
    """aka the 'result' monad"""
    x: Exception|T = wrapped(None)
    if(isinstance(x, Exception)):
        return wrapper(x)
    else:
        return then(wrapper(x), f)


if __name__ == "__main__":
    def succ_of(n: int) -> Callable[[Any], int|ValueError]:
        if n <= 0:
            return wrapper(ValueError("Only positive integers have predecessors"))
        else:
            return wrapper(n-1)

    def to_float(n: int) -> Callable[[Any], float|RuntimeError]:
        if n == 1:
            return wrapper(RuntimeError("Idk bro")) 
        else:
            return wrapper(float(n))

    def inverse(x: float) -> Callable[[Any], str|ZeroDivisionError]: 
        if x == 0:
            return wrapper(ZeroDivisionError("Zero does not have an inverse")) 
        else:
            return wrapper(f"{1 / x:.3f}")

    n1: Callable[[Any], int] = wrapper(5)
    s1: str|Exception = either(
        either(
            either(
                n1,
                succ_of
            ),
            to_float
        ),
        inverse
    )(None)

    assert isinstance(s1, str)
    assert s1 == f"{1 / (5 - 1):.3f}"
    print("s1:", s1)

    n2: Callable[[Any], int] = wrapper(0)
    s2: str|Exception = either(
        either(
            either(
                n2,
                succ_of
            ),
            to_float
        ),
        inverse
    )(None)

    assert isinstance(s2, Exception)
    print("s2:", s2)

    n3: Callable[[Any], int] = wrapper(2)
    s3: str|Exception = either(
        either(
            either(
                n3,
                succ_of
            ),
            to_float
        ),
        inverse
    )(None)

    assert isinstance(s3, Exception)
    print("s3:", s3)

    n4: Callable[[Any], int] = wrapper(1)
    s4: str|Exception = either(
        either(
            either(
                n4,
                succ_of
            ),
            to_float
        ),
        inverse
    )(None)

    assert isinstance(s4, Exception)
    print("s4:", s4)
    

