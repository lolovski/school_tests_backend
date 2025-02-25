from datetime import datetime
from typing import List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base
from models.card import CardUser


class Problem(Base):
    __tablename__ = "problem"
    name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(255))
    difficulty_level_id: Mapped[Optional[int]] = mapped_column(ForeignKey("difficulty_level.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("problem_category.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    memory_limit: Mapped[Optional[int]] = mapped_column(Integer)
    time_limit: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tests: Mapped[List['Test']] = relationship(
        "Test",
        back_populates="problem"
    )
    category: Mapped['ProblemCategory'] = relationship(
        "ProblemCategory",
        back_populates="problems"
    )
    users: Mapped[List['User']] = relationship(
        secondary="user_problem",
        back_populates="problems"
    )
    user_problems: Mapped[List['UserProblem']] = relationship(
        back_populates="problem",
    )


class Test(Base):
    __tablename__ = "test"
    problem_id: Mapped[int] = mapped_column(ForeignKey("problem.id"))
    input_data: Mapped[str] = mapped_column(String(2048))
    output_data: Mapped[str] = mapped_column(String(2048))

    problem: Mapped["Problem"] = relationship(
        "Problem",
        back_populates="tests"
    )
    user_tests: Mapped[List['UserTest']] = relationship(
        'UserTest',
        back_populates='test',
        cascade='all',
        lazy='selectin'
    )


class UserProblem(Base):
    __tablename__ = "user_problem"

    user_id: Mapped[int] = mapped_column(ForeignKey(
            "user.id",
            ondelete='CASCADE'
        )
    )
    problem_id: Mapped[int] = mapped_column(ForeignKey(
            "problem.id",
            ondelete='CASCADE'
        )
    )
    solved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now())
    solution: Mapped[Optional[str]] = mapped_column(String(16000))
    attempt: Mapped[int] = mapped_column(Integer, default=1)
    problem: Mapped['Problem'] = relationship(
        back_populates="user_problems"
    )
    user: Mapped['User'] = relationship(
        back_populates="problem_users"
    )
    verdict: Mapped[Optional[str]] = mapped_column(String(128))


class UserTest(Base):
    __tablename__ = "user_test"

    user_id: Mapped[int] = mapped_column(ForeignKey(
            "user.id",
            ondelete='CASCADE'
        )
    )
    test_id: Mapped[int] = mapped_column(ForeignKey(
            "test.id",
            ondelete='CASCADE'
        )
    )
    problem_id: Mapped[int] = mapped_column(ForeignKey(
            "problem.id",
            ondelete='CASCADE'
        )
    )
    attempt: Mapped[int] = mapped_column(Integer, default=1)
    verdict: Mapped[Optional[str]] = mapped_column(String(128))
    memory: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    time: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    user_output: Mapped[Optional[str]] = mapped_column(String(16000), default="Ответа нет")
    test: Mapped['Test'] = relationship(
        "Test",
        back_populates="user_tests"
    )


class ProblemCategory(Base):
    __tablename__ = "problem_category"
    name: Mapped[str] = mapped_column(String(128))
    level: Mapped[int] = mapped_column(Integer, default=1)
    parent_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('problem_category.id'), default=0)

    problems: Mapped[List['Problem']] = relationship(
        'Problem',
        back_populates='category',
        cascade='all',
        lazy='selectin'
    )
    parent_category: Mapped['ProblemCategory'] = relationship(
        'ProblemCategory',
        back_populates='children_categories',
        remote_side='ProblemCategory.id',
    )
    children_categories: Mapped[List['ProblemCategory']] = relationship(
        'ProblemCategory',
        back_populates='parent_category',
        cascade='all',
        lazy='selectin'
    )
