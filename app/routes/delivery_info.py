from fastapi import APIRouter, status, Depends
from app.dependencies.auth import get_current_user
from app.schema.delivery_info import (
    ShowDeliveryInfoDetails,
    AddDeliveryInfoSchema,
)
from app.service.delivery_info import (
    add_delivery_info_details,
)

deliveryInfoRouter = APIRouter()


@deliveryInfoRouter.post(
    "/addDeliveryInfo",
    status_code=status.HTTP_200_OK,
    response_model=ShowDeliveryInfoDetails,
    description="Add delivery info details",
)
async def add_delivery_info(delivery_info: AddDeliveryInfoSchema, user_data=Depends(get_current_user)):
    delivery_info_data = await add_delivery_info_details(delivery_info, user_data.id)
    return delivery_info_data
