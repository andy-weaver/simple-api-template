import asyncio
from dataclasses import dataclass
from mock_api.models.task import Task
from mock_api.models.task_error import TaskError
from mock_api.models.task_result import TaskResult

@dataclass
class Dag:
    _list: list[Task] = []

    @property
    def tasks(self):
        return self._list

    @property
    def names(self) -> list[str] | list[None]:
        return [x.name for x in self.tasks]

    def __add__(self, other: Task):
        self._list += [other]

    def __call__(self):
        return self._list

    def __repr__(self):
        inner = self.names.join(", ")
        return f"Dag({inner})"

    def __str__(self):
        return self.__repr__()

    def add(
        self, 
        name: str, 
        func: Callable[..., asyncio.Future],
        dependencies: Optional[str | list[str]] = None
    ):
        if dependencies is None:
            self._list += [Task(name, func)]
        elif isinstance(dependencies, str):
            dependencies = [dependencies]
            
        self._list += [Task(name, func, dependencies)]
