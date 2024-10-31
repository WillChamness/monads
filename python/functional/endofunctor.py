from typing import TypeVar, Callable, Any
from functor import wrapper, map

T = TypeVar("T")

def endofunctor(wrapped: Callable[[Any], T], f: Callable[[T], T]) -> Callable[[Any], T]: 
    return map(wrapped, f)


if __name__ == "__main__":
    k: int = endofunctor(
        endofunctor(
            endofunctor(
                wrapper(4),
                lambda n : n+1
            ),
            lambda n : 5*n
        ),
        lambda n : n // 2
    )(None)

    print(k)
    assert k == (5 * (4 + 1)) // 2
