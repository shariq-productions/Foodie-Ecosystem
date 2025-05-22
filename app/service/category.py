from fastapi import HTTPException
from beanie import PydanticObjectId
from app.schema.category import (
    ShowCategoryDetails,
    AddCategorySchema,
    ViewAllCategorySchema,
)
from app.models.category import CategoryDetailsModel


async def add_category_details(category=AddCategorySchema) -> ShowCategoryDetails:

    category_detail_doc = ShowCategoryDetails(
        category_name=category.category_name,
        category_description=category.category_description,
        image_url=category.image_url,
    )
    try:
        await category_detail_doc.insert()
        return ShowCategoryDetails(
            id=category_detail_doc.id, category_name=category_detail_doc.category_name
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def edit_category(
    category_id: PydanticObjectId, category: AddCategorySchema
) -> ShowCategoryDetails:
    category_doc = await CategoryDetailsModel.get(category_id)
    if not category_doc:
        raise HTTPException(status_code=404, detail="Category not found")
    category_doc.category_name = category.category_name
    category_doc.category_description = category.category_description
    category_doc.image_url = category.image_url
    try:
        await category_doc.save()
        return ShowCategoryDetails(
            id=category_doc.id,
            category_name=category_doc.category_name,
            category_description=category_doc.category_description,
            image_url=category_doc.image_url,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def delete_category(category_id: PydanticObjectId) -> dict:
    category_doc = await CategoryDetailsModel.get(category_id)
    if not category_doc:
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        await category_doc.delete()
        return {"detail": "Category deleted successfully"}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def view_all_categories() -> list[ViewAllCategorySchema]:
    try:
        categories = await CategoryDetailsModel.find_all().to_list()
        return [
            ViewAllCategorySchema(
                id=cat.id,
                category_name=cat.category_name,
                category_description=cat.category_description,
                image_url=cat.image_url,
            )
            for cat in categories
        ]
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
