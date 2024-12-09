from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.card import Card, CardTask
from models.class_ import Class
from requests.base import RequestsBase


class CardRequests(RequestsBase):
    ...


card_requests = CardRequests(Card)

class CardTaskRequests(RequestsBase):
    ...

card_task_requests = CardTaskRequests(CardTask)