from beanie import Document, Indexed
from pydantic import EmailStr, Field
from pymongo import ASCENDING


class UserDetailModel(Document):
    email: Indexed(EmailStr, unique=True, index_type=ASCENDING)  # type: ignore
    password: str = Field(..., min_length=8)

    class Settings:
        name = "user"
