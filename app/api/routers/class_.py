from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session
from requests.class_ import class_requests
from app.schemes.class_ import ClassRead, ClassCreate, ClassUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=List[ClassRead],
)
async def get_classes(
    session: AsyncSession = Depends(get_async_session),
):
    classes = await class_requests.get_multi(session=session)
    return classes


@router.get(
    '/{class_id}',
    response_model=ClassRead,
)
async def get_class(
    class_id: int = Path(...),
    session: AsyncSession = Depends(get_async_session),
):
    class_ = await class_requests.get(class_id, session=session)
    return class_


@router.post(
    '/',
    response_model=ClassRead,
)
async def create_class(
    class_: ClassCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_class_name_duplicate(class_.name, session=session)
    db_class = await class_requests.create(class_, session=session)
    return db_class


@router.patch(
    '/{class_id}',
    response_model=ClassRead,
)
async def update_class(
        class_id: int,
        update_in: ClassUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    class_ = await check_class_exists(class_id, session=session)
    if update_in.name is not None:
        await check_class_name_duplicate(name=update_in.name, session=session)
    class_ = await class_requests.update(class_, update_in, session=session)
    return class_


@router.delete(
    '/{class_id}',
    response_model=ClassRead,
    response_model_exclude_none=True,
)
async def delete_class(
        class_id: int = Path(...),
        session: AsyncSession = Depends(get_async_session),
):
    class_ = await check_class_exists(class_id, session=session)
    class_ = await class_requests.remove(class_, session=session)
    return class_


async def check_class_name_duplicate(
    name: str,
    session: AsyncSession,
) -> None:
    duplicate_class = await class_requests.get_by_name(name=name, session=session)
    if duplicate_class is not None:
        raise HTTPException(status_code=400, detail="Class already registered")


async def check_class_exists(
        class_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    class_ = await class_requests.get(obj_id=class_id, session=session)
    if class_ is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_