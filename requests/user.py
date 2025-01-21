from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.class_ import Class
from models.user import User
from requests.base import RequestsBase
from sqlalchemy import select, asc
from sqlalchemy.orm import joinedload


class UserRequests(RequestsBase):
    async def get_students(
            self,
            session: AsyncSession,
    ):
        query = (
            select(User)
            .options(joinedload(User.class_))  # Предполагая, что связь называется class_
            .join(Class)
            .order_by(asc(Class.name))
        )
        result = await session.execute(query)
        return result.unique().scalars().all()


user_requests = UserRequests(User)