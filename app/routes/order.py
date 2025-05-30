from app.dependencies.auth import get_current_user
from fastapi import APIRouter, status, Depends
from app.schema.order import (
    ShowOrderDetails,
)
from app.service.order import (
    add_order_details,
    view_orders_by_user,
    view_orders_by_admin,
    update_status,
)
from beanie import PydanticObjectId

orderRouter = APIRouter()


@orderRouter.post(
    "/addOrder",
    status_code=status.HTTP_200_OK,
    response_model=ShowOrderDetails,
    description="Add order details",
)
async def add_order(user_data=Depends(get_current_user)):
    order_data = await add_order_details(user_data.id)
    return order_data


@orderRouter.put(
    "/updateStatus/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowOrderDetails,
    description="Update order status",
)
async def update_order_status(order_id: PydanticObjectId, status: str):
    return await update_status(order_id, status)


@orderRouter.get(
    "/viewOrdersByUser/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowOrderDetails],
    description="View orders by user",
)
async def get_orders_by_user(user_id: PydanticObjectId):
    return await view_orders_by_user(user_id)


@orderRouter.get(
    "/viewOrdersByAdmin/{admin_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowOrderDetails],
    description="View orders by admin",
)
async def get_orders_by_admin(admin_id: PydanticObjectId):
    return await view_orders_by_admin(admin_id)
