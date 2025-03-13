from pydantic import BaseModel


class TaskResult(BaseModel):
    operation: str
    result: int