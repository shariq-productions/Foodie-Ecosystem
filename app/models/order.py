from beanie import Document, Link
from pydantic import Field, root_validator
from typing import List
from app.models.user import UserDetailModel, UserType
from datetime import datetime
from app.schema.order import OrderItemSchema


class OrderDetailsModel(Document):
    user_id: Link[UserDetailModel] = Field(..., alias="user_id")
    admin_id: Link[UserDetailModel] = Field(..., alias="admin_id")
    items: List[OrderItemSchema]
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @root_validator(pre=True)
    def check_admin_type(cls, values):
        admin = values.get("admin_id")
        # If admin is a Link, it may not be populated yet; check if populated
        if hasattr(admin, "type"):
            if admin.user_type != UserType.ADMIN:
                raise ValueError("admin_id must reference a user of type 'admin'")
        return values

    class Settings:
        name = "order"
