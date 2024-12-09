from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
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



