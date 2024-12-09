from datetime import datetime
from typing import List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base


class Card(Base):
    __tablename__ = "card"
    name: Mapped[Optional[str]] = mapped_column(String(128), default=None)
    variant: Mapped[Optional[str]] = mapped_column(Integer, nullable=True)
    tasks: Mapped[List['Task']] = relationship(
        back_populates='cards',
        secondary='card_task'
    )


class CardTask(Base):
    __tablename__ = 'card_task'
    id = None
    card_id: Mapped[int] = mapped_column(ForeignKey(
        'card.id',
        ondelete='CASCADE'
    ), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey(
        'task.id',
        ondelete='CASCADE'
    ), primary_key=True)