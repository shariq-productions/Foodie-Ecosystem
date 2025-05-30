from app.models.item import ItemDetailsmModel
from fastapi import HTTPException
from beanie import PydanticObjectId
from beanie.operators import In
from app.schema.cart import ShowCartDetails
from app.models.cart import CartDetailsModel
from collections import defaultdict


async def add_cart_details(
    item_id: PydanticObjectId, user_id: PydanticObjectId
) -> ShowCartDetails:
    # Check if the item exists in the cart for the user
    print("Item ID:", item_id)
    print("User ID:", user_id)
    cart_item = await CartDetailsModel.find_one(
        (
            CartDetailsModel.user_id.id == user_id
            if hasattr(CartDetailsModel.user_id, "id")
            else CartDetailsModel.user_id == user_id
        ),
        (
            CartDetailsModel.item_id.id == item_id
            if hasattr(CartDetailsModel.item_id, "id")
            else CartDetailsModel.item_id == item_id
        ),
    )
    print(cart_item)
    if cart_item:
        print("I am here")
        # Increment quantity by 1
        cart_item.quantity += 1
        await cart_item.save()
        return ShowCartDetails(id=cart_item.id)
    else:
        # Get item price
        item = await ItemDetailsmModel.get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        cart_detail_doc = CartDetailsModel(
            user_id=user_id,
            item_id=item_id,
            quantity=1,
            price=item.cost,
        )
        await cart_detail_doc.insert()
        return ShowCartDetails(id=cart_detail_doc.id)


async def remove_item_from_cart(
    user_id: PydanticObjectId, item_id: PydanticObjectId
) -> dict:
    cart_item = await CartDetailsModel.find_one(
        (
            CartDetailsModel.user_id.id == user_id
            if hasattr(CartDetailsModel.user_id, "id")
            else CartDetailsModel.user_id == user_id
        ),
        (
            CartDetailsModel.item_id.id == item_id
            if hasattr(CartDetailsModel.item_id, "id")
            else CartDetailsModel.item_id == item_id
        ),
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        await cart_item.save()
        return {"detail": "Cart item quantity decreased by 1"}
    else:
        await cart_item.delete()
        return {"detail": "Cart item removed from cart"}


async def remove_items_from_cart(
    user_id: PydanticObjectId, item_id: PydanticObjectId
) -> dict:
    try:
        result = await CartDetailsModel.find(
            (
                CartDetailsModel.user_id.id == user_id
                if hasattr(CartDetailsModel.user_id, "id")
                else CartDetailsModel.user_id == user_id
            ),
            (
                CartDetailsModel.item_id.id == item_id
                if hasattr(CartDetailsModel.item_id, "id")
                else CartDetailsModel.item_id == item_id
            ),
        ).delete()
        return {"detail": f"{result.deleted_count} cart items removed successfully"}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def view_cart(user_id: PydanticObjectId):
    cart_items = await CartDetailsModel.find(
        CartDetailsModel.user_id.id == user_id
        if hasattr(CartDetailsModel.user_id, "id")
        else CartDetailsModel.user_id == user_id
    ).to_list()
    if not cart_items:
        return {"cart_id": None, "user_id": user_id, "admin": []}

    item_ids = [
        cart_item.item_id.ref.id if hasattr(cart_item.item_id, "ref") else cart_item.item_id
        for cart_item in cart_items
    ]

    items = await ItemDetailsmModel.find(In(ItemDetailsmModel.id, item_ids)).to_list()
    item_map = {str(item.id): item for item in items}
    print("Item Map:", item_map)

    grouped = defaultdict(list)
    for cart_item in cart_items:
        # Always convert cart_item.item_id to string for lookup
        item_id_str = str(cart_item.item_id.ref.id if hasattr(cart_item.item_id, "ref") else cart_item.item_id)
        item = item_map.get(item_id_str)
        if not item:
            continue
        admin_id = str(item.user_id.ref.id if hasattr(item.user_id, "ref") else item.user_id)
        grouped[admin_id].append(
            {
                "item_id": item_id_str,
                "item_name": item.item_name,
                "quantity": cart_item.quantity,
                "price": cart_item.price,
            }
        )

    admin = [
        {"admin_id": admin_id, "items": items}
        for admin_id, items in grouped.items()
    ]

    cart_id = str(cart_items[0].id) if cart_items else None

    return {
        "cart_id": cart_id,
        "user_id": str(user_id),
        "admin": admin
    }