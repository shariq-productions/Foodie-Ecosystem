from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.auth import login_for_access_token
from app.schema.user import (
    ShowUserDetails,
    AddUserSchema,
    ChangePasswordSchema,
)
from app.schema.auth import Token
from app.service.user import (
    add_user_details,
    delete_user_by_id,
    update_user_password_by_id,
)
from beanie import PydanticObjectId

userRouter = APIRouter()


@userRouter.post(
    "/signUp",
    status_code=status.HTTP_200_OK,
    response_model=ShowUserDetails,
    description="Add user deatils",
)
async def add_user(user: AddUserSchema):
    user_data = await add_user_details(
        user.email, user.password, user.name, user.user_type
    )
    return user_data


@userRouter.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: PydanticObjectId):
    return await delete_user_by_id(user_id)


@userRouter.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: PydanticObjectId,
    data: ChangePasswordSchema,
    description="Route to update the user password",
):
    return await update_user_password_by_id(user_id, data)


@userRouter.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token_route(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    return await login_for_access_token(form_data.username, form_data.password)
