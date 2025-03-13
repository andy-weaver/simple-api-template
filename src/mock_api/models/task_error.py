from __future__ import annotations
from pydantic import BaseModel, Field

class TaskError(BaseModel):
    code: int
    message: str | Callable[..., str]
