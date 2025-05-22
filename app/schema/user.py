from pydantic import BaseModel, Field, EmailStr
from beanie import PydanticObjectId, Indexed
from pymongo import ASCENDING
from app.models.user import UserType


class ShowUserDetails(BaseModel):
    id: PydanticObjectId


class AddUserSchema(BaseModel):
    email: Indexed(EmailStr, unique=True, index_type=ASCENDING)  # type: ignore
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=3)
    user_type: UserType = Field(
        ..., description="Type of user: admin, customer, vendor"
    )


class ChangePasswordSchema(BaseModel):
    password: str = Field(..., min_length=8)
