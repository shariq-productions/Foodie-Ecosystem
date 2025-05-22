from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class ShowItemDetails(BaseModel):
    id: PydanticObjectId
    item_name: str = Field(..., example="Spegety")


class AddItemSchema(BaseModel):
    item_name: str = Field(..., example="Spegety")
    item_description: str = Field(..., example="Spegety is a type of pasta")
    image_url: str = Field(..., example="https://example.com/image.jpg")
    cost: float = Field(..., example=10.99)
    category_id: PydanticObjectId
    user_id: PydanticObjectId
    rating: float = Field(..., example=4.5)


class ViewAllItemsByUserIdSchema(AddItemSchema):
    id: PydanticObjectId


class ViewAllItemsSchema(ViewAllItemsByUserIdSchema):
    product_count: int = Field(..., example=10)
