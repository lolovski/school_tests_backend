from datetime import datetime
from typing import List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base


class Task(Base):
    __tablename__ = "task"
    name: Mapped[Optional[str]] = mapped_column(String(128), default=None)
    number: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    answer: Mapped[Optional[str]] = mapped_column(String(128), default=None)
    text: Mapped[Optional[str]] = mapped_column(String(1024), default=None)
    solution_url: Mapped[Optional[str]] = mapped_column(String(256), default=None)

    difficulty_level_id: Mapped[Optional[int]] = mapped_column(ForeignKey("difficulty_level.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('task_category.id'))

    category: Mapped[Optional['TaskCategory']] = relationship(
        'TaskCategory',
        back_populates='tasks',
    )
    difficulty_level: Mapped[Optional['DifficultyLevel']] = relationship(
        'DifficultyLevel',
        back_populates='tasks',
    )
    images: Mapped[Optional['TaskImage']] = relationship(
        'TaskImage',
        back_populates='task',
        cascade='all',
        lazy='selectin'
    )
    cards: Mapped[List['Card']] = relationship(
        back_populates='tasks',
        secondary='card_task'
    )
    users: Mapped[List['User']] = relationship(
        back_populates='tasks',
        secondary='user_task',
    )
    card_tasks: Mapped[List['CardTask']] = relationship(
        back_populates='task',
    )
    user_tasks: Mapped[List['UserTask']] = relationship(
        back_populates='task'
    )


class TaskCategory(Base):
    __tablename__ = "task_category"
    name: Mapped[str] = mapped_column(String(128))
    level: Mapped[int] = mapped_column(Integer, default=1)
    parent_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('task_category.id'), default=None)

    tasks: Mapped[List['Task']] = relationship(
        'Task',
        back_populates='category',
        cascade='all',
        lazy='selectin'
    )
    parent_category: Mapped['TaskCategory'] = relationship(
        'TaskCategory',
        back_populates='children_categories',
        remote_side='TaskCategory.id',
    )
    children_categories: Mapped[List['TaskCategory']] = relationship(
        'TaskCategory',
        back_populates='parent_category',
        cascade='all',
        lazy='selectin'
    )


class DifficultyLevel(Base):
    __tablename__ = "difficulty_level"
    name: Mapped[str] = mapped_column(String(128))

    tasks: Mapped[List['Task']] = relationship(
        'Task',
        back_populates='difficulty_level',
        cascade='all',
        lazy='selectin'
    )


class ImageCategory(Base):
    __tablename__ = 'image_category'
    name: Mapped[str] = mapped_column(String(128))

    images: Mapped[List['TaskImage']] = relationship(
        'TaskImage',
        back_populates='category',
        cascade='all',
        lazy='selectin'
    )


class TaskImage(Base):
    __tablename__ = 'task_image'
    url: Mapped[Optional[str]] = mapped_column(String(256), default=None)
    file_path: Mapped[str] = mapped_column(String(1024))
    category_id: Mapped[int] = mapped_column(ForeignKey('image_category.id'))
    task_id: Mapped[int] = mapped_column(ForeignKey('task.id'))

    task: Mapped['Task'] = relationship(
        'Task',
        back_populates='images'
    )
    category: Mapped['ImageCategory'] = relationship(
        'ImageCategory',
        back_populates='images'
    )


class UserTask(Base):
    __tablename__ = "user_task"
    id = None
    user_id: Mapped[int] = mapped_column(ForeignKey(
        'user.id',
        ondelete='CASCADE'
    ), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey(
        'task.id',
        ondelete='CASCADE'
    ), primary_key=True)
    user_answer: Mapped[str] = mapped_column(String(512))
    card_id: Mapped[Optional[int]] = mapped_column(ForeignKey('card.id'), default=None, primary_key=True)

    task: Mapped['Task'] = relationship(
        back_populates='user_tasks'
    )
    user: Mapped['User'] = relationship(
        back_populates='task_users'
    )
