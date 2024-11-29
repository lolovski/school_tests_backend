from fastapi import APIRouter, Depends

from core.auth import auth_backend
from core.user_manager import fastapi_users, current_user
from models.user import User
from app.schemes.user import UserRead, UserCreate, UserUpdate

router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth/reset-password",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth/verify",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)


@router.get("/authenticated-route", tags=["auth"])
async def authenticated_route(user: User = Depends(current_user)):
    return {"message": f"Hello {user.email}!"}


@router.get(
    "/users/me",
    tags=['users'],
    response_model=UserRead,
            )
async def get_current_user(user: User = Depends(current_user)):
    return user

"""@router.post(
    '/',
    response_model=UserRead,
    response_description='Краткое описаие пользователя',
    summary='Создание нового пользователя',
    response_model_exclude_none=True,
)
async def create_user_api(
        user: UserCreate = Body(..., openapi_examples=user_create_examples),
        session: AsyncSession = Depends(get_async_session),
):
   
        Создание пользователя:

        - **username**: ник
        - **password**: пароль
        - **last_name**: фамилия
        - **first_name**: имя
        - **middle_name**: отчество
        - **class_user**: ID класса
   
    db_user = await get_user_by_username(user.username, session=session)
    if db_user:
        raise HTTPException(status_code=400, detail='User already registered')
    db_user = await create_user(user, session=session)
    return db_user"""

