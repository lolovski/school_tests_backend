from typing import Dict, Union
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.card import Card, CardTask, CardUser
from models.class_ import Class
from models.task import Task, UserTask
from models.user import User
from requests.base import RequestsBase


class CardRequests(RequestsBase):
    ...


card_requests = CardRequests(Card)

class CardTaskRequests(RequestsBase):
    async def get(
            self,
            session: AsyncSession,
            task_id: int = None,
            card_id: int = None,
    ):
        if task_id is not None and card_id is not None:

            card_task = await session.scalar(
                select(self.model)
                .where(
                    self.model.task_id == task_id,
                    self.model.card_id == card_id,
                )
            )

            return card_task
        elif task_id is not None and card_id is None:
            card_task = await session.scalars(
                select(self.model)
                .where(
                    self.model.task_id == task_id,
                )
            )
        elif card_id is not None and task_id is None:
            card_task = await session.scalars(
                select(self.model)
                .where(
                    self.model.card_id == card_id,
                )
            )
        else:
            card_task = await session.scalars(
                select(CardTask)
            )

        return card_task.all()


card_task_requests = CardTaskRequests(CardTask)


class CardUserRequests(RequestsBase):

    async def get(
            self,
            session: AsyncSession,
            card_id: int = None,
            user_id: int = None,
    ):
        card_user = await session.scalar(
            select(CardUser)
            .where(
                CardUser.card_id == card_id,
                CardUser.user_id == user_id,
            )
        )
        return card_user

    async def get_for_card(
            self,
            user_id: int,
            card_id: int,
            session: AsyncSession,
    ):
        card = await session.scalar(
            select(Card)
            .where(
                Card.id == card_id,
            )
            .options(selectinload(Card.tasks).selectinload(Task.user_tasks.and_(
                UserTask.user_id == user_id,
                UserTask.card_id == card_id,
            )))
        )
        return card

    async def get_multi_user(
            self,
            user_id: int,
            session: AsyncSession,
    ):
        user_cards = await session.scalars(
            select(self.model)
            .where(self.model.user_id == user_id)
            .options(selectinload(self.model.card))
        )
        return user_cards.all()

    async def get_multi_card(
            self,
            card_id: int,
            session: AsyncSession,
    ):
        card_users = await session.scalars(
            select(self.model)
            .where(
                self.model.card_id == card_id,
            )
        )
        return card_users.all()


card_user_requests = CardUserRequests(CardUser)