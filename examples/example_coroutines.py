from enum import StrEnum, auto
from time import time

from generator import BaseGenerator, YieldFrom
from coroutine import EventLoop


class AsyncSleep(BaseGenerator):
    """Fake async sleep"""

    def __init__(self, amount):
        self._started_on = time()
        self._amount = amount

    def _next(self):
        if time() - self._started_on >= self._amount:
            raise StopIteration


class SomeTask(BaseGenerator):
    def __init__(self):
        self._context_position = 0

    def _next(self):
        """
        print('Started SomeTask')
        await sleep(15)
        print('Middle of SomeTask')
        await sleep(2)
        print('Finished SomeTask')
        """

        context_position = self._context_position

        if context_position == 0:
            print('Started SomeTask')
            self._context_position += 1
            return YieldFrom(AsyncSleep(15))

        if context_position == 1:
            print('Middle of SomeTask')
            self._context_position += 1
            return YieldFrom(AsyncSleep(2))

        print('Finished SomeTask')

        raise StopIteration


class ComplexTask(BaseGenerator):
    class ContextPosition(StrEnum):
        FIRST = auto()
        LOOP = auto()
        AFTER = auto()
        LAST = auto()

    def __init__(self):
        self._context_position = ComplexTask.ContextPosition.FIRST

    def _next(self):
        """
        print('Started ComplexTask')
        await sleep(5)
        print('Looping ComplexTask')
        for i in range(5):
            print(i)
            await sleep(.1)
        await sleep(2)
        print('Finished ComplexTask')
        return 'Very Important Value'
        """

        if self._context_position == ComplexTask.ContextPosition.FIRST:
            print('Started ComplexTask')
            self._context_position = ComplexTask.ContextPosition.LOOP
            self._loop_counter = 0
            return YieldFrom(AsyncSleep(5))

        if self._context_position == ComplexTask.ContextPosition.LOOP:
            if self._loop_counter < 5:
                print('Looping ComplexTask')
                print(self._loop_counter)
                self._loop_counter += 1
                return YieldFrom(AsyncSleep(.1))

            self._context_position = ComplexTask.ContextPosition.AFTER

        if self._context_position == ComplexTask.ContextPosition.AFTER:
            self._context_position = ComplexTask.ContextPosition.LAST
            return YieldFrom(AsyncSleep(2))

        if self._context_position == ComplexTask.ContextPosition.LAST:
            print('Finished ComplexTask')
            stop_iteration = StopIteration()
            stop_iteration.value = 'Very Important Value'

            raise stop_iteration


tasks = [
    SomeTask(),
    ComplexTask(),
    ComplexTask(),
    SomeTask()
]

event_loop = EventLoop()

event_loop.add_tasks(*tasks)

event_loop.run_until_complete()
