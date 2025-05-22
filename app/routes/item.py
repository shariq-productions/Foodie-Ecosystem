from app.dependencies.auth import get_current_user
from fastapi import APIRouter, status, Depends
from app.schema.item import (
    ShowItemDetails,
    AddItemSchema,
)
from app.service.item import (
    add_item_details,
    viewAllItems,
    viewAllItemByUserId,
    updateItem,
    deleteItem,
)
from beanie import PydanticObjectId

itemRouter = APIRouter()


@itemRouter.post(
    "/addItem",
    status_code=status.HTTP_200_OK,
    response_model=ShowItemDetails,
    description="Add user deatils",
)
async def add_item(item: AddItemSchema):
    item_data = await add_item_details(item)
    return item_data


@itemRouter.get(
    "/viewAllItems", status_code=status.HTTP_200_OK, description="View all items"
)
async def get_all_items(user_data=Depends(get_current_user)):
    return await viewAllItems(user_data.id)


@itemRouter.get(
    "/viewAllItemByUserId",
    status_code=status.HTTP_200_OK,
    description="View all items by user id",
)
async def get_items_by_user(user_data=Depends(get_current_user)):
    return await viewAllItemByUserId(user_data.id)


@itemRouter.put(
    "/updateItem/{item_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowItemDetails,
    description="Update item",
)
async def update_item(item_id: PydanticObjectId, item: AddItemSchema):
    return await updateItem(item_id, item)


@itemRouter.delete(
    "/deleteItem/{item_id}", status_code=status.HTTP_200_OK, description="Delete item"
)
async def delete_item(item_id: PydanticObjectId):
    return await deleteItem(item_id)
