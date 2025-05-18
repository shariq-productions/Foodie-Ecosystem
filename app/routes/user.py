from fastapi import APIRouter
from app.schema.user import (
    ShowUserDetails,
    AddUserSchema,
)
from app.service.user import (
    add_user_details,
)

userRouter = APIRouter()


@userRouter.post("/", response_model=ShowUserDetails, description="Add user deatils")
async def add_user(user: AddUserSchema):
    user_data = await add_user_details(user.email, user.password)
    return user_data
