from enum import Enum
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from pymongo import ASCENDING
from datetime import datetime


class UserType(str, Enum):

    ADMIN = "admin"
    CUSTOMER = "customer"
    VENDOR = "vendor"


class UserDetailModel(Document):
    email: Indexed(EmailStr, unique=True, index_type=ASCENDING)  # type: ignore
    password: str = Field(..., min_length=8)
    name: str
    user_type: str = Field(..., description="Type of user: admin, customer, vendor")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "user"
