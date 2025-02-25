from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.class_ import Class
from requests.base import RequestsBase


class ClassRequests(RequestsBase):
    ...


class_requests = ClassRequests(Class)