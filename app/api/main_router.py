from fastapi import APIRouter

from app.api.routers.user import router as user_router
from app.api.routers.class_ import router as class_router
main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(class_router, prefix="/class", tags=["class"])

