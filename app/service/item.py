from app.models.cart import CartDetailsModel
from fastapi import HTTPException
from app.schema.item import (
    ShowItemDetails,
    AddItemSchema,
    ViewAllItemsByUserIdSchema,
    ViewAllItemsSchema,
)
from app.models.item import ItemDetailsmModel
from beanie import PydanticObjectId


async def add_item_details(item: AddItemSchema, user_id) -> ShowItemDetails:

    item_detail = ItemDetailsmModel(
        item_name=item.item_name,
        item_description=item.item_description,
        cost=item.cost,
        rating=item.rating,
        image_url=item.image_url,
        user_id=user_id,
        category_id=item.category_id,
    )
    try:
        await item_detail.insert()
        return item_detail

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def viewAllItems(user_id: PydanticObjectId) -> list[ViewAllItemsSchema]:
    try:
        items = await ItemDetailsmModel.find_all().to_list()
        item_list = []
        for item in items:
            quantity = await CartDetailsModel.find_one(
                (
                    CartDetailsModel.user_id.id == user_id
                    if hasattr(CartDetailsModel.user_id, "id")
                    else CartDetailsModel.user_id == user_id
                ),
                (
                    CartDetailsModel.item_id.id == item.id
                    if hasattr(CartDetailsModel.item_id, "id")
                    else CartDetailsModel.item_id == item.id
                ),
            )
            item_list.append(
                ViewAllItemsSchema(
                    id=item.id,
                    item_name=item.item_name,
                    item_description=item.item_description,
                    cost=item.cost,
                    rating=item.rating,
                    image_url=item.image_url,
                    user_id=(
                        item.user_id.ref.id
                        if hasattr(item.user_id, "ref") and item.user_id.ref
                        else item.user_id
                    ),
                    category_id=(
                        item.category_id.ref.id
                        if hasattr(item.category_id, "ref") and item.category_id.ref
                        else item.category_id
                    ),
                    product_count=quantity.quantity if quantity else 0,
                )
            )

        return item_list
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def viewAllItemByUserId(
    user_id: PydanticObjectId,
) -> list[ViewAllItemsByUserIdSchema]:
    try:
        items = await ItemDetailsmModel.find_all().to_list()
        return [
            ViewAllItemsByUserIdSchema(
                id=item.id,
                item_name=item.item_name,
                item_description=item.item_description,
                cost=item.cost,
                rating=item.rating,
                image_url=item.image_url,
                user_id=(
                    item.user_id.ref.id
                    if hasattr(item.user_id, "ref") and item.user_id.ref
                    else item.user_id
                ),
                category_id=(
                    item.category_id.ref.id
                    if hasattr(item.category_id, "ref") and item.category_id.ref
                    else item.category_id
                ),
            )
            for item in items
        ]
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def updateItem(item_id: PydanticObjectId, item: AddItemSchema, user_id) -> ShowItemDetails:
    item_detail = await ItemDetailsmModel.get(item_id)
    if not item_detail:
        raise HTTPException(status_code=404, detail="Item not found")
    item_detail.item_name = item.item_name
    item_detail.item_description = item.item_description
    item_detail.cost = item.cost
    item_detail.rating = item.rating
    item_detail.image_url = item.image_url
    item_detail.user_id = user_id
    item_detail.category_id = item.category_id
    try:
        await item_detail.save()
        return ShowItemDetails(id=item_detail.id, item_name=item_detail.item_name)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def deleteItem(item_id: PydanticObjectId) -> dict:
    try:
        item_detail = await ItemDetailsmModel.get(item_id)
        if not item_detail:
            raise HTTPException(status_code=404, detail="Item not found")
        await item_detail.delete()
        return {"detail": "Item deleted successfully"}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error deleting item")
