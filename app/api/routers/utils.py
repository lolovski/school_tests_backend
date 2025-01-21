from typing import Dict, Union, List

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


async def check_duplicate(
        requests,
        session: AsyncSession = Depends(get_async_session),
        **kwargs: Dict,
) -> None:
    obj = await requests.get(session=session, **kwargs)
    if obj is not None or (isinstance(obj, list) and len(obj) != 0):
        raise HTTPException(status_code=400, detail="Object already exists")


async def check_object_exists(
        requests,
        session: AsyncSession = Depends(get_async_session),
        **kwargs: Dict,
) -> Union[List, object]:
    obj = await requests.get(**kwargs, session=session)
    if obj is None or (isinstance(obj, list) and len(obj) == 0):
        raise HTTPException(status_code=400, detail="Object not found")
    return obj