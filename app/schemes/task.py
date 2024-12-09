from typing import Optional

from fastapi import Body
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    name: Optional[str] = Field(None)
    number: Optional[int] = Field(None)
    answer: Optional[str] = Field(None)
    text: Optional[str] = Field(None)
    solution_url: Optional[str] = Field(None)

    difficulty_level_id: Optional[int] = Field(None)
    category_id: Optional[int] = Field(None)


class TaskRead(TaskCreate):
    id: int = Field(...)

    class Config:
        orm_mode = True


class TaskUpdate(TaskCreate):
    ...


class TaskCategoryCreate(BaseModel):
    name: Optional[str] = Field(None)
    level: Optional[int] = Field(None)
    parent_category_id: Optional[int] = Field(None)


class TaskCategoryRead(TaskCategoryCreate):
    id: int = Field(...)

    class Config:
        orm_mode = True


class TaskCategoryUpdate(TaskCategoryCreate):
    ...


class DifficultyLevelCreate(BaseModel):
    name: str = Field(...)


class DifficultyLevelRead(DifficultyLevelCreate):
    id: int = Field(...)

    class Config:
        orm_mode = True


class DifficultyLevelUpdate(DifficultyLevelCreate):
    ...


class ImageCategoryCreate(BaseModel):
    name: str = Field(...)


class ImageCategoryRead(ImageCategoryCreate):
    id: int = Field(...)

    class Config:
        orm_mode = True


class ImageCategoryUpdate(ImageCategoryCreate):
    ...


class TaskImageCreate(BaseModel):
    file_path: str = Field(...)
    url: Optional[str] = Field(None)
    category_id: int = Field(...)
    task_id: int = Field(...)


class TaskImageRead(TaskImageCreate):
    id: int = Field(...)

    class Config:
        orm_mode = True


class TaskImageUpdate(TaskImageCreate):
    ...


