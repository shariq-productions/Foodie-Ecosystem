from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import List


class OrderItemSchema(BaseModel):
    item_id: PydanticObjectId
    item_name: str = Field(..., example="Spaghetti")
    quantity: int = Field(..., example=2)
    price: float = Field(..., example=10.99)
    total_amount: float = Field(..., example=21.98)


class ShowOrderDetails(BaseModel):
    id: PydanticObjectId


class AddOrderSchema(BaseModel):
    user_id: PydanticObjectId
    admin_id: PydanticObjectId
    items: List[OrderItemSchema]
    status: str = Field(..., example="pending")
