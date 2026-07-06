from __future__ import annotations
from typing import Generic, TypeVar
from pydantic import BaseModel
T = TypeVar("T")
class OkResponse(BaseModel, Generic[T]):
    ok: bool = True
    data: T | None = None
class ErrorResponse(BaseModel):
    ok: bool = False; error: str; error_code: str | None = None; details: dict | None = None
class PageMeta(BaseModel):
    page: int = 1; page_size: int = 20; total: int = 0
