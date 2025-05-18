from fastapi import APIRouter
from app.routes.user import userRouter

router = APIRouter()

router.include_router(userRouter, prefix="/user", tags=["user"])
