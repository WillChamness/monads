from __future__ import annotations
from typing import TypeVar, Generic, Callable, Any

L = TypeVar("L")
R = TypeVar("R")
T = TypeVar("T")
TSuccess = TypeVar("TSuccess")

class Either(Generic[L, R]):
    def ok(self) -> bool:
        raise NotImplementedError("Please do not initialize Either directly")

    def then(self, f: Callable[[R], Either[L, TSuccess]]) -> Either[L, TSuccess]:
        raise NotImplementedError("Please do not initiialze Either directly")

    def unwrap(self) -> L|R:
        raise NotImplementedError("Please do not initiialze Either directly")

    @staticmethod
    def left(val: L) -> Either[L, Any]:
        return _Left(val)

    @staticmethod
    def right(val: R) -> Either[Any, R]:
        return _Right(val)


class _Left(Either[L, R]):
    def __init__(self, val: L):
        self._val = val

    def ok(self) -> bool:
        return False

    def then(self, f: Callable[[R], Either[L, TSuccess]]) -> Either[L, TSuccess]:
        return Either.left(self._val)

    def unwrap(self) -> L|R:
        return self._val


class _Right(Either[L, R]):
    def __init__(self, val: R):
        self._val = val

    def ok(self) -> bool:
        return True 

    def then(self, f: Callable[[R], Either[L, TSuccess]]) -> Either[L, TSuccess]:
        x: R = self._val
        y: Either[L, TSuccess] = f(x)
        return y

    def unwrap(self) -> L|R:
        return self._val


if __name__ == "__main__":
    def predecessor(n: int) -> Either[Exception, int]:
        if n <= 0:
            return Either.left(ValueError("Only positive integers have predecessors"))
        else:
            return Either.right(n-1)

    def to_float(n: int) -> Either[Exception, float]:
        if n == 1:
            return Either.left(RuntimeError("Idk bro")) 
        else:
            return Either.right(float(n))

    def inverse(x: float) -> Either[Exception, str]: 
        if x == 0:
            return Either.left(ZeroDivisionError("Zero does not have an inverse")) 
        else:
            return Either.right(f"{1 / x:.3f}")

    s1: Either[Exception, str] = Either.right(5).then(predecessor).then(to_float).then(inverse)
    assert s1.ok()
    assert isinstance(s1.unwrap(), str)
    assert s1.unwrap() == f"{1 / (5 - 1):.3f}"
    print("s1:", s1.unwrap())

    s2: Either[Exception, str] = Either.right(0).then(predecessor).then(to_float).then(inverse)
    assert not s2.ok()
    assert isinstance(s2.unwrap(), Exception)
    print("s2:", s2.unwrap())

    s3: Either[Exception, str] = Either.right(2).then(predecessor).then(to_float).then(inverse)
    assert not s3.ok()
    assert isinstance(s3.unwrap(), Exception)
    print("s3:", s3.unwrap())

    s4: Either[Exception, str] = Either.right(1).then(predecessor).then(to_float).then(inverse)
    assert not s4.ok()
    assert isinstance(s4.unwrap(), Exception)
    print("s4:", s4.unwrap())
    






