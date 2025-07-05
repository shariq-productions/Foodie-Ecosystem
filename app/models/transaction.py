from app.models.user import UserDetailModel
from beanie import Document, Link
from pydantic import Field
from datetime import datetime


class TransactionModel(Document):
    user_id: Link[UserDetailModel] = Field(..., alias="user_id")
    amount: float
    payment_method: str
    user_type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "transaction"
