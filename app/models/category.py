from beanie import Document
from pydantic import Field
from datetime import datetime


class CategoryDetailsModel(Document):
    category_name: str
    category_description: str
    image_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "category"
