from app.dependencies.auth import get_current_user
from fastapi import APIRouter, status, Depends
from app.schema.cart import (
    ShowCartDetails,
    ViewCartResponse
)
from app.service.cart import (
    add_cart_details,
    remove_item_from_cart,
    remove_items_from_cart,
    view_cart,
)
from beanie import PydanticObjectId

cartRouter = APIRouter()


@cartRouter.post(
    "/addToCart/{item_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowCartDetails,
    description="Add cart details",
)
async def add_cart(item_id: PydanticObjectId, user_data=Depends(get_current_user)):
    cart_data = await add_cart_details(item_id, user_data.id)
    return cart_data


@cartRouter.delete(
    "/removeItemFromCart/{item_id}",
    status_code=status.HTTP_200_OK,
    description="Remove or decrement item from cart",
)
async def remove_item(item_id: PydanticObjectId, user_data=Depends(get_current_user)):
    return await remove_item_from_cart(user_data.id, item_id)


@cartRouter.delete(
    "/removeItemsFromCart/{item_id}",
    status_code=status.HTTP_200_OK,
    description="Remove all items from user's cart",
)
async def remove_items(item_id: PydanticObjectId, user_data=Depends(get_current_user)):
    return await remove_items_from_cart(user_data.id, item_id)


@cartRouter.get(
    "/viewCart", status_code=status.HTTP_200_OK, description="View cart by user id",
    response_model=ViewCartResponse
)
async def view_cart_route(user_data=Depends(get_current_user)):

    return await view_cart(user_data.id)
