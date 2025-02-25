from datetime import datetime
from typing import List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base
from models.problem import UserProblem


class User(SQLAlchemyBaseUserTable[int], Base):
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)

    last_name: Mapped[str] = mapped_column(String(64))
    first_name: Mapped[str] = mapped_column(String(64))
    middle_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, default=None)

    telegram_id: Mapped[str] = mapped_column(String(64), nullable=True)
    class_id: Mapped[Optional[int]] = mapped_column(ForeignKey('class.id'), default=None, nullable=True)
    status_id: Mapped[Optional[int]] = mapped_column(ForeignKey('status.id'), default=1)

    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    class_: Mapped['Class'] = relationship(
        'Class',
        back_populates='users'
    )
    status: Mapped['Status'] = relationship(
        'Status',
        back_populates='users'
    )
    tasks: Mapped[List['Task']] = relationship(
        back_populates='users',
        secondary='user_task'
    )
    cards: Mapped[List['Card']] = relationship(
        back_populates='users',
        secondary='card_user'
    )
    card_users: Mapped[List['CardUser']] = relationship(
        back_populates='user'
    )
    task_users: Mapped[List['UserTask']] = relationship(
        back_populates='user'
    )
    problems: Mapped[List['Problem']] = relationship(
        back_populates='users',
        secondary='user_problem'
    )
    problem_users: Mapped[List['UserProblem']] = relationship(
        back_populates='user'
    )



class Status(Base):
    __tablename__ = 'status'
    name: Mapped[str] = mapped_column(String(128))
    level: Mapped[int] = mapped_column(Integer)

    users: Mapped[List["User"]] = relationship(
        'User',
        back_populates='status',
        cascade='all'
    )