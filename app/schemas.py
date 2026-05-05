from pydantic import BaseModel
from typing import Any


class IncidentQuestionRequest(BaseModel):
    question: str


class IncidentQuestionResponse(BaseModel):
    answer: str
    sources: list[dict[str, Any]]