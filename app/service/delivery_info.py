from fastapi import HTTPException
from app.schema.delivery_info import ShowDeliveryInfoDetails, AddDeliveryInfoSchema
from app.models.delivery_info import DeliveryInfoDetailsModel


async def add_delivery_info_details(
    delivery_info: AddDeliveryInfoSchema,
) -> ShowDeliveryInfoDetails:
    delivery_info_doc = DeliveryInfoDetailsModel(
        first_name=delivery_info.first_name,
        last_name=delivery_info.last_name,
        email_address=delivery_info.email_address,
        street=delivery_info.street,
        city=delivery_info.city,
        state=delivery_info.state,
        zip_code=delivery_info.zip_code,
        country=delivery_info.country,
        phone_number=delivery_info.phone_number,
        user_id=delivery_info.user_id,
    )
    try:
        await delivery_info_doc.insert()
        return ShowDeliveryInfoDetails(
            id=delivery_info_doc.id, user_id=delivery_info_doc.user_id.ref.id
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
