from __future__ import annotations
from typing import TypeVar, Generic, Callable
from functor import Functor

T = TypeVar("T")
U = TypeVar("U")

class Monad(Generic[T]):
    def __init__(self, val: T):
        self._func = Functor(val)

    def then(self, f: Callable[[T], Monad[U]]) -> Monad[U]:
        y: Functor[Monad[U]] = self._func.map(f)
        return y.val

    def val(self) -> T:
        return self._func.val


if __name__ == "__main__":
    def hello_world(s: str) -> Monad[str]: 
        return Monad(s + " world")

    def duplicate_string(s: str) -> Monad[str]:
        return Monad(s + s)

    def count_chars(s: str) -> Monad[int]:
        def count(s: str) -> int:
            if s == "":
                return 0
            else:
                return 1 + count(s[1:])

        return Monad(count(s))

    def div_3(n: int) -> Monad[float]:
        return Monad(n / 3)

    result: Monad[float] = Monad("hello").then(hello_world).then(duplicate_string).then(count_chars).then(div_3)
    assert result.val() == len(("hello" + " world")*2) / 3

