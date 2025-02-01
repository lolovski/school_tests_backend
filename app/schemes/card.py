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
    category_id: Optional[int] = Field(
        None,
    )
    is_active: Optional[bool] = Field(
        True,
    )


class CardRead(CardCreate):
    id: int

    class Config:
        orm_mode = True


class CardUpdate(BaseModel):
    name: Optional[str] = Body(None)
    variant: Optional[int] = Body(None)
    category_id: Optional[int] = Field(
        None,
    )

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


class CardCategoryCreate(BaseModel):
    name: Optional[str] = Field(None)
    parent_category_id: Optional[int] = Field(None)


class CardCategoryRead(CardCategoryCreate):
    id: int = Field(...)
    level: int = Field(...)

    class Config:
        orm_mode = True


class CardCategoryUpdate(CardCategoryCreate):
    ...



