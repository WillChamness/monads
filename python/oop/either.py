from __future__ import annotations
from typing import TypeVar, Generic, Callable

T = TypeVar("T")
U = TypeVar("U")

class Either(Generic[T]):
    def __init__(self, val: Exception|T):
        self._val = val

    def then(self, f: Callable[[T], Either[U]]) -> Either[U]:
        if isinstance(self._val, Exception):
            return Either(self._val)
        else:
            return f(self._val)

    def val(self) -> Exception|T:
        return self._val

    def ok(self) -> bool:
        return not isinstance(self._val, Exception)


if __name__ == "__main__":
    def succ_of(n: int) -> Either[int]:
        if n <= 0:
            return Either(ValueError("Only positive integers have predecessors"))
        else:
            return Either(n-1)

    def to_float(n: int) -> Either[float]:
        if n == 1:
            return Either(RuntimeError("Idk bro")) 
        else:
            return Either(float(n))

    def inverse(x: float) -> Either[str]: 
        if x == 0:
            return Either(ZeroDivisionError("Zero does not have an inverse")) 
        else:
            return Either(f"{1 / x:.3f}")

    s1: Either[str] = Either(5).then(succ_of).then(to_float).then(inverse)
    assert s1.ok()
    assert isinstance(s1.val(), str)
    assert s1.val() == f"{1 / (5 - 1):.3f}"
    print("s1:", s1.val())

    s2: Either[str] = Either(0).then(succ_of).then(to_float).then(inverse)
    assert not s2.ok()
    assert isinstance(s2.val(), Exception)
    print("s2:", s2.val())

    s3: Either[str] = Either(2).then(succ_of).then(to_float).then(inverse)
    assert not s3.ok()
    assert isinstance(s3.val(), Exception)
    print("s3:", s3.val())

    s4: Either[str] = Either(1).then(succ_of).then(to_float).then(inverse)
    assert not s4.ok()
    assert isinstance(s4.val(), Exception)
    print("s4:", s4.val())
    






