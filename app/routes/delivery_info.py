from fastapi import APIRouter, status
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
async def add_delivery_info(delivery_info: AddDeliveryInfoSchema):
    delivery_info_data = await add_delivery_info_details(delivery_info)
    return delivery_info_data
