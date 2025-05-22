from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class ShowCategoryDetails(BaseModel):
    id: PydanticObjectId
    category_name: str = Field(..., example="Spegety")


class AddCategorySchema(BaseModel):
    category_name: str = Field(..., example="Spegety")
    category_description: str = Field(..., example="Spegety is a type of pasta")
    image_url: str = Field(..., example="https://example.com/image.jpg")


class ViewAllCategorySchema(ShowCategoryDetails):
    category_description: str = Field(..., example="Spegety is a type of pasta")
    image_url: str = Field(..., example="https://example.com/image.jpg")
