from abc import ABC, abstractmethod
from typing import Any, Self, Iterable


class BaseGenerator(ABC):
    def __new__(cls, *args: Any, **kwargs: Any):
        g = super().__new__(cls)
        g._close = False
        g._throw = None
        g._send = None
        g.__yield_from__ = None
        return g

    @abstractmethod
    def _next(self):
        """
        Body of generator function.
        Should raise StopIteration, if generator ends.
        """

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Any:
        if self._close:
            raise StopIteration

        if (__yield_from__ := self.__yield_from__) is not None:
            try:
                return next(__yield_from__)
            except StopIteration:
                self.__yield_from__ = None
                return next(self)

        try:
            r = self._next()
        except StopIteration:
            self._closed = True
            raise

        if isinstance(r, YieldFrom):
            self.__yield_from__ = r
            return next(self)

        return r

    def close(self) -> None:
        self._close = True

    def send(self, value: Any) -> Any:
        self._send = value
        return next(self)

    def throw(self, exception: BaseException) -> None:
        raise NotImplementedError


class YieldFrom:
    def __init__(self, iterable: Iterable) -> None:
        self._iterator = iter(iterable)

    def __next__(self) -> Any:
        return next(self._iterator)
