from beanie import Document, Indexed, Link
from pydantic import EmailStr, Field
from pymongo import ASCENDING
from datetime import datetime
from app.models.user import UserDetailModel


class DeliveryInfoDetailsModel(Document):

    first_name: str
    last_name: str
    email_address: Indexed(EmailStr, unique=False, index_type=ASCENDING)  # type: ignore
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    phone_number: str = Field(..., min_length=9)
    user_id: Link[UserDetailModel] = Field(..., alias="user_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "delivery_info"
