from http import HTTPStatus

from typing import List
from fastapi.params import Query
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routers.utils import check_object_exists, check_name_duplicate
from db.session import get_async_session
from requests.class_ import class_requests
from app.schemes.task import *
from requests.task import *

router = APIRouter()


@router.get(
    "/task/",
    response_model=List[TaskRead],
    tags=['task']
)
async def get_tasks(
        category_id: Optional[int] = Query(None),
        session: AsyncSession = Depends(get_async_session),
):
    tasks = await task_requests.get_multi(session=session, category_id=category_id)
    return tasks


@router.get(
    '/task/{task_id}',
    response_model=TaskRead,
    tags=['task']
)
async def get_task(
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    task = await task_requests.get(task_id, session=session)
    if task is None:
        raise HTTPException(404, detail="Task not found")
    return task


@router.post(
    '/task/',
    response_model=TaskRead,
    tags=['task']
)
async def create_task(
        task: TaskCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(name=task.name, requests=task_requests, session=session)
    db_task = await task_requests.create(obj_in=task, session=session)
    return db_task


@router.patch(
    '/task/{task_id}',
    response_model=TaskRead,
    tags=['task']
)
async def update_task(
        task_id: int,
        update_in: TaskUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    task = await check_object_exists(id=task_id, requests=task_requests, session=session)

    if update_in.name is not None:
        await check_name_duplicate(name=update_in.name, requests=task_requests, session=session)
    task = await task_requests.update(task, update_in, session=session)
    return task


@router.delete(
    '/task/{task_id}',
    response_model=TaskRead,
    response_model_exclude_none=True,
    tags=['task']
)
async def delete_task(
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    task = await check_object_exists(id=task_id, requests=task_requests, session=session)
    task = await task_requests.remove(task, session=session)
    return task


@router.get(
    '/task/card/',
    tags=['task']
)
async def get_card_tasks(
        card_id: str = Query(...),
        session: AsyncSession = Depends(get_async_session),
):

    tasks = await task_requests.get_card_tasks(int(card_id), session=session)

    return tasks


@router.get(
    "/task_category/",
    response_model=List[TaskCategoryRead],
    tags=['task category']
)
async def get_task_categories(
        parent_category_id: Optional[int] = Query(None),
        session: AsyncSession = Depends(get_async_session),
):
    task_categories = await task_category_requests.get_multi(session=session, parent_category_id=parent_category_id)
    return task_categories


@router.get(
    '/task_category/{task_category_id}',
    response_model=TaskCategoryRead,
    tags=['task category']
)
async def get_task_category(
        task_category_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    task_category = await task_category_requests.get(task_category_id, session=session)
    if task_category is None:
        raise HTTPException(404, detail="Task category not found")
    return task_category


@router.post(
    '/task_category/',
    response_model=TaskCategoryRead,
    tags=['task category']
)
async def create_task_category(
        task_category: TaskCategoryCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(name=task_category.name, requests=task_category_requests, session=session)
    db_task_category = await task_category_requests.create(obj_in=task_category, session=session)
    return db_task_category


@router.patch(
    '/task_category/{task_category_id}',
    response_model=TaskCategoryRead,
    tags=['task category']
)
async def update_task_category(
        task_category_id: int,
        update_in: TaskCategoryUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    task_category = await check_object_exists(id=task_category_id, requests=task_category_requests, session=session)

    if update_in.name is not None:
        await check_name_duplicate(name=update_in.name, requests=task_category_requests, session=session)
    task_category = await task_category_requests.update(task_category, update_in, session=session)
    return task_category


@router.delete(
    '/task_category/{task_category_id}',
    response_model=TaskCategoryRead,
    response_model_exclude_none=True,
    tags=['task category']
)
async def delete_task_category(
        task_category_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    task_category = await check_object_exists(id=task_category_id, requests=task_category_requests, session=session)
    task_category = await task_requests.remove(task_category, session=session)
    return task_category


@router.get(
    "/difficulty_level/",
    response_model=List[DifficultyLevelRead],
    tags=['difficulty level']

)
async def get_difficulty_levels(
        session: AsyncSession = Depends(get_async_session),
):
    difficulty_levels = await difficulty_level_requests.get_multi(session=session)
    return difficulty_levels


@router.get(
    '/difficulty_level/{difficulty_level_id}',
    response_model=DifficultyLevelRead,
    tags=['difficulty level']
)
async def get_difficulty_level(
        difficulty_level_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    difficulty_level = await difficulty_level_requests.get(difficulty_level_id, session=session)
    if difficulty_level is None:
        raise HTTPException(404, detail="Difficulty level not found")
    return difficulty_level


@router.post(
    '/difficulty_level/',
    response_model=DifficultyLevelRead,
    tags=['difficulty level']
)
async def create_difficulty_level(
        difficulty_level: DifficultyLevelCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(name=difficulty_level.name, requests=difficulty_level_requests, session=session)
    db_difficulty_level = await difficulty_level_requests.create(obj_in=difficulty_level, session=session)
    return db_difficulty_level


@router.patch(
    '/difficulty_level/{difficulty_level_id}',
    response_model=DifficultyLevelRead,
    tags=['difficulty level']
)
async def update_difficulty_level(
        difficulty_level_id: int,
        update_in: DifficultyLevelUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    difficulty_level = await check_object_exists(id=difficulty_level_id, requests=difficulty_level_requests, session=session)

    if update_in.name is not None:
        await check_name_duplicate(name=update_in.name, requests=difficulty_level_requests, session=session)
    difficulty_level = await difficulty_level_requests.update(difficulty_level, update_in, session=session)
    return difficulty_level


@router.delete(
    '/difficulty_level/{difficulty_level_id}',
    response_model=DifficultyLevelRead,
    response_model_exclude_none=True,
    tags=['difficulty level']
)
async def delete_difficulty_level(
        difficulty_level_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    difficulty_level = await check_object_exists(id=difficulty_level_id, requests=difficulty_level_requests, session=session)
    difficulty_level = await difficulty_level_requests.remove(difficulty_level, session=session)
    return difficulty_level


@router.get(
    '/user_task/user',
    response_model=List[TaskUserRead],
    tags=['user_task']
)
async def get_user_tasks(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    user_tasks = await user_task_requests.get_multi_user(user_id=user_id, session=session)

    return user_tasks


@router.get(
    '/user_task/task',
    response_model=List[TaskUserRead],
    tags=['user_task']
)
async def get_task_users(
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    task_users = await user_task_requests.get_multi_task(task_id=task_id, session=session)
    return task_users


@router.get(
    '/user_task/',
    response_model=TaskUserRead,
    tags=['user_task']
)
async def get_user_task(
        user_id: int = Query(...),
        task_id: int = Query(...),
        session: AsyncSession = Depends(get_async_session),
):
    user_task = await user_task_requests.get(user_id=user_id, task_id=task_id, session=session)
    if user_task is None:
        raise HTTPException(404, detail="User task not found")
    return user_task

@router.post(
    '/user_task/',
    response_model=TaskUserRead,
    tags=['user_task']
)
async def create_user_task(
        user_task: TaskUserCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_user_task_duplicate(user_id=user_task.user_id, task_id=user_task.task_id, card_id=user_task.card_id, session=session)
    db_user_task = await user_task_requests.create(obj_in=user_task, session=session)
    return db_user_task


@router.patch(
    '/user_task/',
    response_model=TaskUserRead,
    tags=['user_task']
)
async def path_user_task(
    update_in: TaskUserUpdate,
    user_id: int = Query(...),
    task_id: int = Query(...),
    session: AsyncSession = Depends(get_async_session),
):
    user_task = await user_task_requests.get(user_id=user_id, task_id=task_id, session=session)
    user_task = await user_task_requests.update(user_task, update_in, session=session)
    return user_task



@router.delete(
    '/user_task/',
    response_model=TaskUserRead,
    response_model_exclude_none=True,
    tags=['user_task']
)
async def delete_user_task(
    user_id: int = Query(...),
    task_id: int = Query(...),
    session: AsyncSession = Depends(get_async_session),
):
    user_task = await user_task_requests.get(user_id=user_id, task_id=task_id, session=session)
    user_task = await user_task_requests.remove(user_task, session=session)
    return user_task


async def check_user_task_duplicate(user_id, task_id, session, card_id=None):
    user_task = await user_task_requests.get(user_id=user_id, task_id=task_id, session=session, card_id=card_id)
    if user_task is not None:
        raise HTTPException(400, detail="User task already exists")