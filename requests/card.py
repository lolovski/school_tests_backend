from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.card import Card, CardTask
from models.class_ import Class
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
        if task_id is None and card_id is None:

            card_task = await session.scalar(
                select(CardTask)
                .where(
                    CardTask.task_id == task_id,
                    CardTask.card_id == card_id,
                )
            )
            return card_task
        elif task_id is not None:
            card_task = await session.scalars(
                select(CardTask)
                .where(
                    CardTask.task_id == task_id,
                )
            )
        elif card_id is not None:
            card_task = await session.scalars(
                select(CardTask)
                .where(
                    CardTask.card_id == card_id,
                )
            )
        else:
            card_task = await session.scalars(
                select(CardTask)
            )
        return card_task.all()


card_task_requests = CardTaskRequests(CardTask)