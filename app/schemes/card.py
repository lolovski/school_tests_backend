from typing import Optional

from fastapi import Body
from pydantic import BaseModel, Field


class CardCreate(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=128,
    )
    variant: Optional[int] = Field(
        None,
    )


class CardRead(CardCreate):
    id: int

    class Config:
        orm_mode = True


class CardUpdate(BaseModel):
    name: Optional[str] = Body(None)
    variant: Optional[int] = Body(None)


class CardTaskCreate(BaseModel):
    card_id: int
    task_id: int


class CardTaskRead(CardTaskCreate):
    class Config:
        orm_mode = True


class CardTaskUpdate(BaseModel):
    card_id: Optional[int] = Body(None)
    tasK_id: Optional[int] = Body(None)


class CardUserCreate(BaseModel):
    user_id: int
    card_id: int


class CardUserRead(CardUserCreate):

    class Config:
        orm_mode = True


class CardUserUpdate(BaseModel):
    user_id: Optional[int] = Body(None)
    card_id: Optional[int] = Body(None)
