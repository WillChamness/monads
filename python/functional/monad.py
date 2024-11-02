from typing import Callable, TypeVar, Any
from functor import map, wrapper

T = TypeVar("T")
U = TypeVar("U")

def then(wrapped: Callable[[Any], T], f: Callable[[T], Callable[[Any], U]]) -> Callable[[Any], U]:
    y: Callable[[Any], Callable[[Any], U]] = map(wrapped, f)
    return y(None)



if __name__ == "__main__":
    def hello_world(s: str) -> Callable[[Any], str]:
        return wrapper(s + " world")

    def duplicate_string(s: str) -> Callable[[Any], str]:
        return wrapper(s + s)

    def count_chars(s: str) -> Callable[[Any], int]:
        def count(s: str) -> int:
            if s == "":
                return 0
            else:
                return 1 + count(s[1:])

        return wrapper(count(s))

    def div_3(n: int) -> Callable[[Any], float]:
        return wrapper(n / 3)

    s: Callable[[Any], str] = wrapper("hello")
    
    x: Callable[[Any], float] = then(
        then(
            then(
                then(
                    s,
                    hello_world
                ),
                duplicate_string,
            ),
            count_chars,
        ),
        div_3
    )

    print(x(None))
    assert x(None) == len(("hello" + " world")*2) / 3

    
