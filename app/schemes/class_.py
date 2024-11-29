from typing import Optional

from fastapi import Body
from pydantic import BaseModel, Field


class ClassCreate(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=32,
    )


class ClassRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ClassUpdate(BaseModel):
    name: Optional[str] = Body(None)
