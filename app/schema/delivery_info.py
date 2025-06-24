from pydantic import BaseModel, Field, EmailStr
from beanie import PydanticObjectId


class ShowDeliveryInfoDetails(BaseModel):
    id: PydanticObjectId
    user_id: PydanticObjectId


class AddDeliveryInfoSchema(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    email_address: EmailStr = Field(..., example="john.doe@example.com")
    street: str = Field(..., example="123 Main St")
    city: str = Field(..., example="New York")
    state: str = Field(..., example="NY")
    zip_code: str = Field(..., example="10001")
    country: str = Field(..., example="USA")
    phone_number: str = Field(..., example="1234567890")

