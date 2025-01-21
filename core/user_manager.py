from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, InvalidPasswordException, FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import auth_backend
from core.config import settings
from db.session import get_async_session
from models.user import User
from app.schemes.user import UserCreate

SECRET = settings.secret_user


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def validate_password(
        self, password: str, user: Union[UserCreate, User]
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"Пользователь {user.email} зарегистрирован.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


