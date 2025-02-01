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
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now())
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)
    description: Mapped[Optional[str]] = mapped_column(String(256), default=None)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('card_category.id'))

    category: Mapped[Optional['CardCategory']] = relationship(
        'CardCategory',
        back_populates='cards'
    )
    #deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

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
    user_task_card: Mapped[List['UserTask']] = relationship(
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
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now())
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


class CardCategory(Base):
    __tablename__ = 'card_category'
    name: Mapped[str] = mapped_column(String(128))
    level: Mapped[int] = mapped_column(Integer, default=0)
    parent_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('card_category.id'), default=0)
    cards: Mapped[List['Card']] = relationship(
        'Card',
        back_populates='category',
        cascade='all',
        lazy='selectin'
    )

    parent_category: Mapped['Optional[CardCategory]'] = relationship(
        back_populates='children_categories',
        remote_side='CardCategory.id'
    )
    children_categories: Mapped[List['CardCategory']] = relationship(
        'CardCategory',
        back_populates='parent_category',
        cascade='all',
        lazy='selectin'
    )
