import contextlib
from typing import Optional

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr
from sqlalchemy import select

from core.config import settings
from core.user_manager import get_user_db, get_user_manager
from db.session import get_async_session

from app.schemes.user import UserCreate
from models.class_ import Class
from models.user import Status

get_async_session_context = contextlib.asynccontextmanager(get_async_session)

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_base_db(

):
    try:
        async with get_async_session_context() as session:
            classes = await session.scalars(select(Class))
            if len(classes.all()) == 0:
                first_class = Class(name=settings.first_class_name)
                session.add(first_class)
                student = Status(name='student', level=1)
                teacher = Status(name='teacher', level=2)
                admin = Status(name='admin', level=3)
                session.add(student)
                session.add(teacher)
                session.add(admin)

                await session.commit()
    except UserAlreadyExists:
        pass




        
async def create_user(
        email: EmailStr,
        password: str,
        last_name: str,
        first_name: str,
        middle_name: str,
        status_id: int,
        class_id: Optional[int] = None,
        is_superuser: bool = False,
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            last_name=last_name,
                            first_name=first_name,
                            middle_name=middle_name,
                            class_id=class_id,
                            status_id=status_id,
                            is_superuser=is_superuser,
                        )
                    )
                    return user
    except UserAlreadyExists:
        pass


async def create_first_user():
    if (settings.first_user_email is not None
            and settings.first_user_password is not None
            and settings.first_user_last_name is not None
            and settings.first_user_first_name is not None
            and settings.first_user_middle_name is not None
            and settings.first_user_class_id is not None
    ):
        await create_user(
            email=settings.first_user_email,
            password=settings.first_user_password,
            last_name=settings.first_user_last_name,
            first_name=settings.first_user_first_name,
            middle_name=settings.first_user_middle_name,
            class_id=settings.first_user_class_id,
            status_id=1,
            is_superuser=True,
        )


async def create_first_superadmin():
    if (settings.first_superadmin_email is not None
            and settings.first_superadmin_password is not None
            and settings.first_superadmin_last_name is not None
            and settings.first_superadmin_first_name is not None
            and settings.first_superadmin_middle_name is not None
    ):
        await create_user(
            email=settings.first_superadmin_email,
            password=settings.first_superadmin_password,
            last_name=settings.first_superadmin_last_name,
            first_name=settings.first_superadmin_first_name,
            middle_name=settings.first_superadmin_middle_name,
            status_id=3,
            is_superuser=True,

        )


async def create_first_teacher():
        await create_user(
            email='teacher@gmail.com',
            password=settings.first_superadmin_password,
            last_name=settings.first_superadmin_last_name,
            first_name=settings.first_superadmin_first_name,
            middle_name=settings.first_superadmin_middle_name,
            status_id=2,
            is_superuser=True,  
        )


async def start_db():
    await create_base_db()
    await create_first_superadmin()
    await create_first_user()
    await create_first_teacher()

