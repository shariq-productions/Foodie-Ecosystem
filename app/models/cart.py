from beanie import Document, Link
from pydantic import Field
from app.models.user import UserDetailModel
from app.models.item import ItemDetailsmModel
from datetime import datetime


class CartDetailsModel(Document):
    user_id: Link[UserDetailModel] = Field(..., alias="user_id")
    item_id: Link[ItemDetailsmModel] = Field(..., alias="item_id")
    quantity: int | None = 0
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "cart"
