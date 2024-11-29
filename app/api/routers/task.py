from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session
from requests.class_ import class_requests
from app.schemes.task import *

router = APIRouter()

@router.get(
    '/{task_id}',
    response_model=TaskRead,
)
async def get_task(
        task_id: int,
):
    ...