from typing import Callable, TypeVar, Any

T = TypeVar("T")
S = TypeVar("S")

def wrapper(x: T) -> Callable[[Any], T]:
    def unwrap(y: Any) -> T:
        return x 

    return unwrap


def map(wrapped: Callable[[Any], T], f: Callable[[T], S]) -> Callable[[Any], S]:
    x: T = wrapped(None)
    y: S = f(x)
    return wrapper(y)


if __name__ == "__main__":
    def half_int(n: int) -> float:
        return 0.5 * n
    def float_as_str(x: float) -> str:
        return f"{x: .2f}"

    n: Callable[[Any], int] = wrapper(7)
    half: Callable[[Any], float] = map(n, half_int)
    to_str: Callable[[Any], str] = map(half, float_as_str)
    s1: str = to_str(None)
    print(s1)

    s2: str = map(
        map(
            wrapper(7),
            half_int
        ),
        float_as_str
    )(None)
    print(s2)
    assert(s1 == s2)

