from typing import Dict, Union, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import and_
from models.card import Card
from models.task import Task, TaskImage, TaskCategory, ImageCategory, DifficultyLevel, UserTask
from requests.base import RequestsBase
from sqlalchemy import desc

class TaskRequests(RequestsBase):
    
    async def get_multi(
            self,
            category_id: int,
            session: AsyncSession,
    ):
        if category_id is None:
            # Если category_id не задан, возвращаем все задания, отсортированные от новых к старым
            query = select(Task).order_by(Task.created_at.desc())
            result = await session.execute(query)
            return result.scalars().unique().all()
    
        # Получаем все дочерние категории рекурсивно
        async def get_all_child_categories(category_id: int) -> List[int]:
            if category_id != 0:
                query = select(TaskCategory).where(TaskCategory.parent_category_id == category_id)
                result = await session.execute(query)
                child_categories = result.scalars().all()
                all_categories = [category_id]
                for child in child_categories:
                    all_categories.extend(await get_all_child_categories(child.id))
                return all_categories
            else:
                return []
        # Получаем все категории, включая дочерние
        all_categories = await get_all_child_categories(category_id)
    
        # Получаем все задания из этих категорий, отсортированные от новых к старым
        query = (
            select(Task)
            .where(Task.category_id.in_(all_categories))
            .order_by(Task.created_at.desc())
        )
        result = await session.execute(query)
        return result.scalars().unique().all()

    async def get_card_tasks(
            self,
            card_id: int,
            session: AsyncSession,
    ):
        query = (
            select(Task)
            .options(selectinload(Task.images))
            .join(Card.tasks)
            .where(Card.id == card_id)
        )
        result = await session.execute(query)
        return result.scalars().unique().all()


task_requests = TaskRequests(Task)


class TaskImageRequests(RequestsBase):
    ...


task_image_requests = TaskImageRequests(TaskImage)


class TaskCategoryRequests(RequestsBase):

    async def get_multi(
            self,
            parent_category_id: int,
            session: AsyncSession,
    ):
        query = select(self.model).where(self.model.id != 0)
        if parent_category_id is not None:
            query = query.where(self.model.parent_category_id == parent_category_id)
        result = await session.execute(query)
        return result.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        category = self.model(**obj_in_data)
        if obj_in.parent_category_id:
            parent_category = await session.scalar(
                select(self.model).where(self.model.id == obj_in.parent_category_id)
            )
            category_level = parent_category.level + 1
            category.level = category_level
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category


task_category_requests = TaskCategoryRequests(TaskCategory)


class ImageCategoryRequests(RequestsBase):
    ...


image_category_requests = ImageCategoryRequests(ImageCategory)


class DifficultyLevelRequests(RequestsBase):
    ...


difficulty_level_requests = DifficultyLevelRequests(DifficultyLevel)


class UserTaskRequests(RequestsBase):
    async def get_multi_user(
            self,
            user_id: int,
            session: AsyncSession,
    ):
        user_tasks = await session.scalars(
            select(self.model)
            .where(self.model.user_id == user_id)
        )
        return user_tasks.all()

    async def get_multi_task(
            self,
            task_id: int,
            session: AsyncSession,
    ):
        task_users = await session.scalars(
            select(self.model)
            .where(self.model.task_id == task_id)
        )
        return task_users.all()

    async def get(
            self,
            session: AsyncSession,
            **kwargs: Dict[str, Union[str, int]]
    ):
        query = select(self.model)
        filter_conditions = []
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                filter_conditions.append(getattr(self.model, key) == value)

        if filter_conditions:
            query = query.where(and_(*filter_conditions))
        result = await session.execute(query)
        return result.scalar()


user_task_requests = UserTaskRequests(UserTask)