from __future__ import annotations
from pydantic import BaseModel
from mock_api.models.request import Request

class Request(BaseModel):
    kwargs: dict[str, Any] = {}