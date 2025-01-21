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
    users: Mapped[List['User']] = relationship(
        back_populates='cards',
        secondary='card_user'
    )
    user_cards: Mapped[List['CardUser']] = relationship(
        back_populates='card',
    )
    task_cards: Mapped[List['CardTask']] = relationship(
        back_populates='card'
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
    card: Mapped['Card'] = relationship(
        back_populates='task_cards'
    )
    task: Mapped['Task'] = relationship(
        back_populates='card_tasks'
    )





class CardUser(Base):
    __tablename__ = 'card_user'
    id = None
    card_id: Mapped[int] = mapped_column(ForeignKey(
        'card.id',
        ondelete='CASCADE'
    ), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        'user.id',
        ondelete='CASCADE'
    ), primary_key=True)
    card: Mapped['Card'] = relationship(
        back_populates='user_cards'
    )
    user: Mapped['User'] = relationship(
        back_populates='card_users'
    )