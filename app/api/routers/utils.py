from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session


async def check_name_duplicate(
        name: str,
        requests,
        session: AsyncSession = Depends(get_async_session),
) -> None:
    duplicate_obj = await requests.get_by_name(name=name, session=session)
    if duplicate_obj is not None:
        raise HTTPException(status_code=400, detail="Object already exists")


async def check_object_exists(
        id: int,
        requests,
        session: AsyncSession = Depends(get_async_session),
):
    obj = await requests.get(id, session=session)
    if obj is None:
        raise HTTPException(status_code=400, detail="Object not found")
    return obj