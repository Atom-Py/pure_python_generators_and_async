from collections import deque


class EventLoop:
    """
    Very naive EventLoop.
    """

    def __init__(self):
        self._tasks = []
        self._results = []
        self._done = False

    def add_task(self, task):
        self._tasks.append(task)
        self._results.append(None)

    def add_tasks(self, *tasks):
        for task in tasks:
            self.add_task(task)

    def run_until_complete(self):
        tasks = self._tasks

        while tasks:
            done_tasks = deque()

            for i, task in enumerate(tasks):
                try:
                    next(task)
                except StopIteration as e:
                    done_tasks.append(i)
                    print(f'{task} done: returned {e.value}')

            while done_tasks:
                del tasks[done_tasks.pop()]

        self._tasks = tasks
        self._done = True
