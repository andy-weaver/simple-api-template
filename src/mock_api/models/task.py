import asyncio
from dataclasses import dataclass
from typing import Callable

@dataclass
class Task:
    name: str
    func: Callable[..., asyncio.Future]
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []