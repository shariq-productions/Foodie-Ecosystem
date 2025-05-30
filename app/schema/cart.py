from pydantic import BaseModel
from typing import List
from beanie import PydanticObjectId


class ShowCartDetails(BaseModel):
    id: PydanticObjectId


class AddCartSchema(BaseModel):
    user_id: PydanticObjectId
    item_id: PydanticObjectId


class CartAdminItem(BaseModel):
    item_id: PydanticObjectId
    item_name: str
    quantity: int
    price: float


class CartAdminGroup(BaseModel):
    admin_id: PydanticObjectId
    items: List[CartAdminItem]


class ViewCartResponse(BaseModel):
    cart_id: PydanticObjectId
    user_id: PydanticObjectId
    admin: List[CartAdminGroup]
