from __future__ import annotations
from typing import TypeVar, Generic, Callable

T = TypeVar("T")
U = TypeVar("U")

class Functor(Generic[T]):
    def __init__(self, val: T):
        self.val = val

    def map(self, f: Callable[[T], U]) -> Functor[U]:
        x: T = self.val
        y: U = f(x)
        return Functor(y)

    def endo(self, f: Callable[[T], T]) -> Functor[T]:
        return self.map(f)


if __name__ == "__main__":
    def half_int(n: int) -> float:
        return 0.5 * n
    def float_as_str(x: float) -> str:
        return f"{x:.2f}"

    n: Functor[int] = Functor(7)
    s1: Functor[str] = n.map(half_int).map(float_as_str)
    assert s1.val == f"{0.5*7:.2f}"

    k1: Functor[int] = Functor(7)
    k2: Functor[int] = k1.endo(lambda n : n+1).endo(lambda n : 5*n).endo(lambda n : n // 2)
    assert k2.val == (5*(7+1)) // 2

