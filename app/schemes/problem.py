from datetime import datetime
from typing import Optional

from fastapi import Body
from pydantic import BaseModel, Field


class ProblemCreate(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=128,
    )
    description: str = Field(
        ..., min_length=2, max_length=1024,
    )
    difficulty_level_id: int = Field(
        ..., gt=0,
    )
    category_id: int = Field(
        ...,
    )
    memory_limit: int = Field(
        ..., gt=0,
    )
    time_limit: int = Field(
        ..., gt=0,
    )


class ProblemRead(ProblemCreate):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class ProblemUpdate(ProblemCreate):
    name: Optional[str] = Field(
        None, min_length=2, max_length=128,
    )


class ProblemCategoryCreate(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=128,
    )
    parent_category_id: Optional[int] = Field(
        0,
    )


class ProblemCategoryRead(ProblemCategoryCreate):
    id: int
    level: int

    class Config:
        orm_mode = True


class ProblemCategoryUpdate(ProblemCategoryCreate):
    ...


class TestCreate(BaseModel):
    problem_id: int = Field(
        ..., gt=0,
    )
    input_data: str = Field(
        ..., max_length=2048,
    )
    output_data: str = Field(
        ..., max_length=2048,
    )


class TestRead(TestCreate):
    id: int

    class Config:
        orm_mode = True


class TestUpdate(TestCreate):
    ...


class UserProblemCreate(BaseModel):
    user_id: int = Field(
        ...
    )
    problem_id: int = Field(
        ...
    )
    solution: str = Field(
        ..., max_length=16000,
    )
    verdict: Optional[str] = Field(
        None, max_length=128,
    )
    attempt: int = Field(
        1, gt=0,
    )


class UserProblemRead(UserProblemCreate):
    id: int

    class Config:
        orm_mode = True


class UserProblemUpdate(UserProblemCreate):
    ...


class UserTestCreate(BaseModel):
    test_id: int
    user_id: int
    problem_id: int
    verdict: str
    time: float
    memory: float
    attempt: int
    user_output: Optional[str] = Field(None)


class UserTestRead(UserTestCreate):

     class Config:
         orm_mode = True


class UserTestUpdate(UserTestCreate):
    ...