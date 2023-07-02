from typing import Callable, Iterable

from generator import BaseGenerator, From


class MyRange(BaseGenerator):
    def __init__(self, start: int | float = 0, end: int | float = None, step: int | float = 1):
        self._start = start
        self._end = end
        self._step = step

    def _next(self):
        start = self._start
        end = self._end
        step = self._step

        if end is None or step > 0 and start < end or step < 0 and start > end:
            self._start += step
        else:
            raise StopIteration

        return start


class Map(BaseGenerator):
    def __init__(self, map_func: Callable, collection: Iterable):
        self._map_func = map_func
        self._collection_iterator = iter(collection)

    def _next(self):
        """
        for item in collection:
            yield map_func(item)
        """

        return self._map_func(next(self._collection_iterator))


class Godless(BaseGenerator):
    def __init__(self):
        self._context_position = 0

    def _next(self):
        if self._context_position == 0:
            self._context_position += 1
            return From(Gen1())
        raise StopIteration


class Gen1(BaseGenerator):
    def __init__(self):
        self._context_position = 0

    def _next(self):
        if self._context_position == 0:
            self._context_position += 1
            return From(Gen2())
        raise StopIteration


class Gen2(BaseGenerator):
    def __init__(self):
        self._context_position = 0

    def _next(self):
        if self._context_position == 0:
            self._context_position += 1
            return From(MyRange(0, 10))
        raise StopIteration


print(*Godless())
print(list(Map(float, ['1', '2.0', '3.1', 4, 5.0, 6.2])))
print(*MyRange(0, 7, 1.5))
