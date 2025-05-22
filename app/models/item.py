from app.models.category import CategoryDetailsModel
from beanie import Document, Link
from pydantic import Field
from app.models.user import UserDetailModel
from datetime import datetime


class ItemDetailsmModel(Document):
    item_name: str = Field(..., max_length=255)
    item_description: str = Field(None, max_length=1024)
    cost: float = Field(...)
    rating: float = Field(None)
    image_url: str = Field(None)
    user_id: Link[UserDetailModel] = Field(..., alias="user_id")
    category_id: Link[CategoryDetailsModel] = Field(..., alias="category_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "items"
