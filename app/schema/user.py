from pydantic import BaseModel, Field, EmailStr
from beanie import PydanticObjectId, Indexed
from pymongo import ASCENDING


class ShowUserDetails(BaseModel):
    id: PydanticObjectId
    email: str


class AddUserSchema(BaseModel):
    email: Indexed(EmailStr, unique=True, index_type=ASCENDING)  # type: ignore
    password: str = Field(..., min_length=8)
