from __future__ import annotations
from pydantic import BaseModel
from mock_api.models import TaskResult, TaskError

class Response(BaseModel):
    result: dict[str, TaskResult | TaskError]