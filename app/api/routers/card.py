from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routers.utils import check_object_exists, check_name_duplicate
from db.session import get_async_session
from requests.card import card_requests, card_task_requests
from app.schemes.card import *
from requests.card import *


router = APIRouter()


@router.get(
    "/card/",
    response_model=List[CardRead],
    tags=['card']
)
async def get_cards(
        session: AsyncSession = Depends(get_async_session),
):
    cards = await card_requests.get_multi(session=session)
    return cards


@router.get(
    '/card/{card_id}',
    response_model=CardRead,
    tags=['card']
)
async def get_card(
        card_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    card = await card_requests.get(card_id, session=session)
    if card is None:
        raise HTTPException(404, detail="Task not found")
    return card


@router.post(
    '/card/',
    response_model=CardRead,
    tags=['card']
)
async def create_card(
        card: CardCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(name=card.name, requests=card_requests, session=session)
    db_card = await card_requests.create(obj_in=card, session=session)
    return db_card


@router.patch(
    '/card/{card_id}',
    response_model=CardRead,
    tags=['card']
)
async def update_card(
        card_id: int,
        update_in: CardUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    card = await check_object_exists(id=card_id, requests=card_requests, session=session)

    if update_in.name is not None:
        await check_name_duplicate(name=update_in.name, requests=card_requests, session=session)
    card = await card_requests.update(card, update_in, session=session)
    return card


@router.delete(
    '/card/{card_id}',
    response_model=CardRead,
    response_model_exclude_none=True,
    tags=['card']
)
async def delete_card(
        card_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    card = await check_object_exists(id=card_id, requests=card_requests, session=session)
    card = await card_requests.remove(card, session=session)
    return card


@router.get(
    "/card_task/",
    response_model=Union[List[CardTaskRead], CardTaskRead],
    tags=['card task']
)
async def get_card_tasks(
        task_id: Optional[int] = Query(None, description="Task ID"),
        card_id: Optional[int] = Query(None, description="Card ID"),
        session: AsyncSession = Depends(get_async_session),
):
    if card_id is not None and task_id is not None:
        cards = await card_task_requests.get(session=session, task_id=task_id, card_id=card_id)
        return cards
    elif task_id is not None:
        cards = await card_task_requests.get(session=session, task_id=task_id)
    elif card_id is not None:
        cards = await card_task_requests.get(session=session, card_id=card_id)
    else:
        cards = await card_task_requests.get_multi(session=session)

    return cards


@router.post(
    '/card_task/',
    response_model=CardTaskRead,
    tags=['card task']
)
async def create_card_task(
        card_task: CardTaskCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_card_task_duplicate(card_id=card_task.card_id,task_id=card_task.task_id, session=session)
    db_card_task = await card_task_requests.create(obj_in=card_task, session=session)
    return db_card_task


@router.patch(
    '/card_task/',
    response_model=CardTaskRead,
    tags=['card task']
)
async def update_card(
        update_in: CardTaskUpdate,
        task_id: int = Query(..., description="Task ID"),
        card_id: int = Query(..., description="Card ID"),
        session: AsyncSession = Depends(get_async_session),
):
    card_task = await check_card_task_exists(task_id=task_id, card_id=card_id, session=session)
    await check_card_task_duplicate(card_id=card_task.card_id, task_id=card_task.task_id, session=session)
    card_task = await card_task_requests.update(card_task, update_in, session=session)
    return card_task


@router.delete(
    '/card_task/',
    response_model=CardTaskRead,
    response_model_exclude_none=True,
    tags=['card task']
)
async def delete_card(
        task_id: int = Query(..., description="Task ID"),
        card_id: int = Query(..., description="Card ID"),
        session: AsyncSession = Depends(get_async_session),
):
    card_task = await check_card_task_exists(task_id=task_id, card_id=card_id, session=session)
    card_task = await card_task_requests.remove(card_task, session=session)
    return card_task


async def check_card_task_exists(
        task_id: int,
        card_id: int,
        session: AsyncSession,
):
    card_task = await card_task_requests.get(session=session, task_id=task_id, card_id=card_id)
    if card_task is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Card task not found")
    return card_task


async def check_card_task_duplicate(
        task_id: int,
        card_id: int,
        session: AsyncSession,
):
    card_task = await card_task_requests.get(session=session, task_id=task_id, card_id=card_id)
    if card_task is not None:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Card task already exists")