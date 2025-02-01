from typing import Dict, Union, List, Optional, Tuple
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from sqlalchemy.sql import and_, not_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.card import Card, CardTask, CardUser, CardCategory
from models.class_ import Class
from models.task import Task, UserTask
from models.user import User
from requests.base import RequestsBase


class CardRequests(RequestsBase):
    async def get_multi(
            self,
            category_id: int,
            session: AsyncSession,
            user_id: Optional[int] = None,
    ):
        if category_id is None:
            # Если category_id не задан, возвращаем все задания, отсортированные от новых к старым
            query = select(Card).order_by(Card.created_at.desc())
        else:
            # Получаем все дочерние категории рекурсивно
            async def get_all_child_categories(category_id: int) -> List[int]:
                query = select(CardCategory).where(CardCategory.parent_category_id == category_id)
                result = await session.execute(query)
                child_categories = result.scalars().all()
                all_categories = [category_id]
                for child in child_categories:
                    all_categories.extend(await get_all_child_categories(child.id))
                return all_categories

            # Получаем все категории, включая дочерние
            all_categories = await get_all_child_categories(category_id)

            # Получаем все задания из этих категорий, отсортированные от новых к старым
            query = (
                select(Card)
                .where(Card.category_id.in_(all_categories))
                .order_by(Card.created_at.desc())
            )

        if user_id is not None:
            # Добавляем условие, чтобы исключить карточки, которые пользователь уже прошел
            subquery = select(CardUser.card_id).where(CardUser.user_id == user_id).scalar_subquery()
            query = query.where(not_(Card.id.in_(subquery)))

        result = await session.execute(query)
        return result.scalars().unique().all()

    async def get_card_users(
            self,
            card_id: int,
            session: AsyncSession,
    ) -> List[Tuple[User, List[Dict], str]]:
        stmt = (
            select(User)
            .join(CardUser)
            .filter(CardUser.card_id == card_id)
            .options(
                selectinload(User.task_users).joinedload(UserTask.task),
                joinedload(User.class_)
            )
        )

        result = await session.execute(stmt)
        users = result.unique().scalars().all()

        for user in users:

            user_tasks = [
                ut
                for ut in user.task_users
                if ut.card_id == card_id
            ]
            user.task_users = [i for i in user_tasks]
        return users

    async def get_user_cards(
            self,
            user_id: int,
            session: AsyncSession,
    ) -> List[Dict]:
        # Получаем все UserTask для пользователя
        user_tasks_stmt = (
            select(UserTask)
            .where(UserTask.user_id == user_id)
            .options(
                joinedload(UserTask.task),
                joinedload(UserTask.card)
            )
        )

        user_tasks_result = await session.execute(user_tasks_stmt)
        user_tasks = user_tasks_result.scalars().all()

        # Создаем словарь для хранения карточек и ответов пользователя
        card_responses = {}

        for user_task in user_tasks:
            card_id = user_task.card_id
            if card_id not in card_responses:
                card_responses[card_id] = {
                    'card': user_task.card,
                    'tasks': []
                }

            task_data = {
                'task': user_task.task,
                'user_task': {
                    user_task.user_answer
                }
            }
            card_responses[card_id]['tasks'].append(task_data)

        return list(card_responses.values())

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


class CardCategoryRequests(RequestsBase):
    async def get_multi(
            self,
            parent_category_id: int,
            session: AsyncSession,
    ):
        query = select(self.model)
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


card_category_requests = CardCategoryRequests(CardCategory)