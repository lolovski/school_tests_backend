from typing import Dict, Union, List, Optional, Tuple
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from sqlalchemy.sql import and_, not_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.card import Card, CardTask, CardUser, CardCategory
from models.class_ import Class
from models.problem import Problem, Test, ProblemCategory, UserProblem, UserTest
from models.task import Task, UserTask
from models.user import User
from requests.base import RequestsBase

class ProblemRequests(RequestsBase):
    async def get_multi(
            self,
            category_id: int,
            session: AsyncSession,
            user_id: Optional[int] = None,
    ):
        if category_id is None:
            # Если category_id не задан, возвращаем все задания, отсортированные от новых к старым
            query = select(Problem).order_by(Problem.created_at.desc())
        else:
            # Получаем все дочерние категории рекурсивно
            async def get_all_child_categories(category_id: int) -> List[int]:
                if category_id != 0:
                    query = select(ProblemCategory).where(ProblemCategory.parent_category_id == category_id)
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
                select(Problem)
                .where(Problem.category_id.in_(all_categories))
                .order_by(Problem.created_at.desc())
            )

        if user_id is not None:
            # Добавляем условие, чтобы исключить карточки, которые пользователь уже прошел
            subquery = select(UserProblem.problem_id).where(UserProblem.user_id == user_id, UserProblem.verdict == 'OK').scalar_subquery()
            query = query.where(not_(Problem.id.in_(subquery)))

        result = await session.execute(query)
        return result.scalars().unique().all()

problem_requests = ProblemRequests(Problem)

class TestRequests(RequestsBase):
    async def get_multi(
            self,
            session: AsyncSession,
            problem_id: Optional[int] = None
    ):
        query = select(self.model)
        if problem_id is not None:
            query = query.where(self.model.problem_id == problem_id)
        result = await session.execute(query)
        return result.scalars().all()

test_requests = TestRequests(Test)

class ProblemCategoryRequests(RequestsBase):
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

problem_category_requests = ProblemCategoryRequests(ProblemCategory)

class UserProblemRequests(RequestsBase):

    async def get(
        self,
        session: AsyncSession,
        user_id: Optional[int] = None,
        problem_id: Optional[int] = None,
        category_id: Optional[int] = None,
    ):
        if user_id and problem_id:
            # Возвращаем список UserProblems для данного user_id и problem_id
            return await self.get_user_problem(session, user_id, problem_id)
        elif problem_id:
            # Возвращаем список пользователей с их UserProblems и UserTests для данного problem_id
            return await self.get_user_problems_by_problem(session, problem_id)
        elif user_id:
            # Возвращаем список Problems, которые решал пользователь, с их UserProblems
            return await self.get_problems_by_user(session, user_id)
        else:
            raise ValueError("Invalid parameters")

    async def get_user_problem(
        self,
        session: AsyncSession,
        user_id: int,
        problem_id: int,
    ):
        # Получаем все UserProblem для данного user_id и problem_id
        query = select(UserProblem).where(
            UserProblem.user_id == user_id,
            UserProblem.problem_id == problem_id
        )
        user_problems = await session.scalars(query)
        user_problems = user_problems.all()

        # Получаем связанные UserTests
        async def get_user_tests(user_id: int, problem_id: int, attempt: int):
            query = select(UserTest).where(
                UserTest.user_id == user_id,
                UserTest.problem_id == problem_id,
                UserTest.attempt == attempt
            )
            result = await session.execute(query)
            return result.scalars().all()

        # Добавляем UserTests к каждому UserProblem
        for user_problem in user_problems:
            user_problem.user_tests = await get_user_tests(user_problem.user_id, user_problem.problem_id, user_problem.attempt)

        return user_problems

    async def get_user_problems_by_problem(
        self,
        session: AsyncSession,
        problem_id: int,
    ):
        # Получаем все UserProblem для данного problem_id
        query = select(UserProblem).where(UserProblem.problem_id == problem_id)
        user_problems = await session.scalars(query)
        user_problems = user_problems.all()

        # Получаем связанные UserTests
        async def get_user_tests(user_id: int, problem_id: int, attempt: int):
            query = select(UserTest).where(
                UserTest.user_id == user_id,
                UserTest.problem_id == problem_id,
                UserTest.attempt == attempt
            ).options(joinedload(UserTest.test))
            result = await session.execute(query)
            return result.scalars().all()

        # Добавляем UserTests к каждому UserProblem
        for user_problem in user_problems:
            user_problem.user_tests = await get_user_tests(user_problem.user_id, user_problem.problem_id, user_problem.attempt)

        # Группируем UserProblem по user_id
        user_dict = {}
        for user_problem in user_problems:
            if user_problem.user_id not in user_dict:
                user_dict[user_problem.user_id] = []
            user_dict[user_problem.user_id].append(user_problem)

        # Преобразуем словарь в список пользователей
        users = []
        for user_id, user_problems in user_dict.items():
            user = await session.scalar(
                select(User).where(User.id == user_id)
                    .options(joinedload(User.class_))
            )
            user.user_problems = user_problems
            users.append(user)

        return users

    async def get_problems_by_user(
        self,
        session: AsyncSession,
        user_id: int,
    ):
        # Получаем все UserProblem для данного user_id
        query = select(UserProblem).where(UserProblem.user_id == user_id)
        user_problems = await session.scalars(query)
        user_problems = user_problems.all()

        # Получаем связанные UserTests
        async def get_user_tests(user_id: int, problem_id: int, attempt: int):
            query = select(UserTest).where(
                UserTest.user_id == user_id,
                UserTest.problem_id == problem_id,
                UserTest.attempt == attempt
            )
            result = await session.execute(query)
            return result.scalars().all()

        # Добавляем UserTests к каждому UserProblem
        for user_problem in user_problems:
            user_problem.user_tests = await get_user_tests(user_problem.user_id, user_problem.problem_id, user_problem.attempt)

        # Группируем UserProblem по problem_id
        problem_dict = {}
        for user_problem in user_problems:
            if user_problem.problem_id not in problem_dict:
                problem_dict[user_problem.problem_id] = []
            problem_dict[user_problem.problem_id].append(user_problem)

        # Преобразуем словарь в список Problems
        problems = []
        for problem_id, problem_users in problem_dict.items():
            problem = await session.get(Problem, problem_id)
            problem.problem_users = problem_users
            problems.append(problem)

        return problems

    async def get_count_attempts(
            self,
            session: AsyncSession,
            user_id: Optional[int] = None,
            problem_id: Optional[int] = None,
    ):
        query = select(UserProblem).where(UserProblem.user_id == user_id).where(UserProblem.problem_id == problem_id)
        user_problems = await session.scalars(query)
        return len(user_problems.all())

user_problem_requests = UserProblemRequests(UserProblem)

class UserTestRequests(RequestsBase):
    ...

user_test_requests = UserTestRequests(UserTest)