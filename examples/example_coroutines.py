from enum import Enum
from time import time

from generator import BaseGenerator, From
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
            return From(AsyncSleep(15))

        if context_position == 1:
            print('Middle of SomeTask')
            self._context_position += 1
            return From(AsyncSleep(2))

        print('Finished SomeTask')

        raise StopIteration


class ComplexTask(BaseGenerator):
    class Context(Enum):
        START = 1
        LOOP = 2
        AFTER_LOOP = 3
        FINISH = 4

    def __init__(self):
        self._context_position = self.Context.START

    def _next(self):
        """
        print('Started ComplexTask')
        await sleep(5)

        print('Looping ComplexTask')
        for i in range(5):
            print(f'{i=}')
            for j in range(2):
                print(f'{j=}')
                await sleep(.1)
            await sleep(.2)

        await sleep(2)

        print('Finished ComplexTask')
        return 'Very Important Value'
        """

        context = self.Context

        match self._context_position:
            case context.START:
                print('Started ComplexTask')
                self._context_position = context.LOOP
                self._i = self._j = 0
                return From(AsyncSleep(5))
            case context.LOOP:
                i, j = self._i, self._j

                while i < 5:
                    print(f'{i=}')
                    while j < 2:
                        print(f'{j=}')
                        self._j += 1
                        return From(AsyncSleep(.1))
                    self._j = 0
                    self._i += 1
                    return From(AsyncSleep(.2))

                self._context_position = context.AFTER_LOOP
            case context.AFTER_LOOP:
                self._context_position = context.FINISH
                return From(AsyncSleep(2))
            case context.FINISH:
                print('Finished ComplexTask')
                stop_iteration = StopIteration()
                stop_iteration.value = 'Very Important Value'
                raise stop_iteration
            case _:
                raise RuntimeError


tasks = [
    SomeTask(),
    ComplexTask(),
    ComplexTask(),
    SomeTask()
]

event_loop = EventLoop()

event_loop.add_tasks(*tasks)

event_loop.run_until_complete()
