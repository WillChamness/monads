from __future__ import annotations
from typing import TypeVar, Generic, Callable

T = TypeVar("T")
U = TypeVar("U")

class _Option(Generic[T]):
    def unwrap(self) -> T|None:
        pass

class _Nothing(_Option):
    def unwrap(self) -> T|None:
        return None

class _Just(_Option):
    def __init__(self, val: T):
        self._val = val

    def unwrap(self) -> T|None:
        return self._val

class Maybe(Generic[T]):
    def __init__(self, val: T|None):
        self._val = val

    def then(self, f: Callable[[T], Maybe[U]]) -> Maybe[U]:
        if self._val is None:
            return Maybe(None)
        else:
            return f(self._val)

    def val(self) -> T|None:
        return self._val



if __name__ == "__main__":
    def succ_of(n: int) -> Maybe[int]:
        if n <= 0:
            return Maybe(None)
        else:
            return Maybe(n-1)

    def to_float(n: int) -> Maybe[float]:
        if n == 1:
            return Maybe(None) 
        else:
            return Maybe(float(n))

    def inverse(x: float) -> Maybe[str]:
        if x == 0:
            return Maybe(None) 
        else:
            return Maybe(f"{1 / x:.3f}")

    s1: Maybe[str] = Maybe(5).then(succ_of).then(to_float).then(inverse)

    assert s1.val() is not None
    assert isinstance(s1.val(), str)
    assert s1.val() == f"{1 / (5 - 1):.3f}"
    print(s1.val())

    s2: Maybe[str] = Maybe(0).then(succ_of).then(to_float).then(inverse)
    assert s2.val() is None

    s3: Maybe[str] = Maybe(2).then(succ_of).then(to_float).then(inverse)
    assert s3.val() is None

    s4: Maybe[str] = Maybe(1).then(succ_of).then(to_float).then(inverse)
    assert s4.val() is None
