from fastapi import APIRouter, status
from app.schema.category import (
    AddCategorySchema,
    ShowCategoryDetails,
)
from app.service.category import (
    add_category_details,
    edit_category,
    delete_category,
    view_all_categories,
)
from beanie import PydanticObjectId

categoryRouter = APIRouter()


@categoryRouter.post(
    "/createCategory",
    status_code=status.HTTP_200_OK,
    response_model=ShowCategoryDetails,
    description="Add user deatils",
)
async def add_category(category: AddCategorySchema):
    user_data = await add_category_details(category)
    return user_data


@categoryRouter.put(
    "/editCategory/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowCategoryDetails,
    description="Edit a category",
)
async def update_category(category_id: PydanticObjectId, category: AddCategorySchema):
    return await edit_category(category_id, category)


@categoryRouter.delete(
    "/deleteCategory/{category_id}",
    status_code=status.HTTP_200_OK,
    description="Delete a category",
)
async def remove_category(category_id: PydanticObjectId):
    return await delete_category(category_id)


@categoryRouter.get(
    "/viewAllCategories",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowCategoryDetails],
    description="View all categories",
)
async def get_all_categories():
    return await view_all_categories()
