from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class RequestsBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.scalar(select(self.model).where(self.model.id == obj_id))
        return db_obj

    async def get_by_name(self, name: str, session: AsyncSession):
        db_obj = await session.scalar(select(self.model).where(self.model.name == name))
        return db_obj

    async def get_multi(
            self,
            session: AsyncSession,
    ):
        db_odjs = await session.scalars(select(self.model))
        return db_odjs.all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        print(obj_in)
        update_data = obj_in.dict(exclude_unset=True)
        print(update_data)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
