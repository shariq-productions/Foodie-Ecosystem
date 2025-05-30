from typing import List
from app.service.cart import view_cart
from fastapi import HTTPException
from app.schema.order import ShowOrderDetails, OrderItemSchema
from app.models.order import OrderDetailsModel
from beanie import PydanticObjectId


async def add_order_details(user_id: PydanticObjectId) -> List[ShowOrderDetails]:

    cart_details = await view_cart(user_id)
    orders_to_create = []
    for admin_group in cart_details["admin"]:
        admin_id = admin_group["admin_id"]
        items = admin_group["items"]

        order_items = [
            OrderItemSchema(
                item_id=item["item_id"],
                item_name=item["item_name"],
                quantity=item["quantity"],
                price=item["price"],
                total_amount=item["quantity"]
                * item["price"],  # assuming total = qty * price
            )
            for item in items
        ]

        order_detail_doc = OrderDetailsModel(
            user_id=cart_details["user_id"],
            admin_id=admin_id,
            items=order_items,
            status="PENDING",  # or any default status you want
        )

        orders_to_create.append(order_detail_doc)
    order_details_list = []
    try:
        for order_doc in orders_to_create:
            await order_doc.insert()
            order_details_list.append(ShowOrderDetails(id=order_doc.id))
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def update_status(order_id: PydanticObjectId, status: str) -> ShowOrderDetails:
    order = await OrderDetailsModel.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    try:
        await order.save()
        return ShowOrderDetails(
            id=order.id,
            user_id=order.user_id,
            admin_id=order.admin_id,
            items=order.items,
            status=order.status,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def view_orders_by_user(user_id: PydanticObjectId) -> list[ShowOrderDetails]:
    try:
        orders = await OrderDetailsModel.find(
            OrderDetailsModel.user_id == user_id
        ).to_list()
        return [
            ShowOrderDetails(
                id=order.id,
                user_id=order.user_id,
                admin_id=order.admin_id,
                items=order.items,
                status=order.status,
            )
            for order in orders
        ]
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def view_orders_by_admin(admin_id: PydanticObjectId) -> list[ShowOrderDetails]:
    try:
        orders = await OrderDetailsModel.find(
            OrderDetailsModel.admin_id == admin_id
        ).to_list()
        return [
            ShowOrderDetails(
                id=order.id,
                user_id=order.user_id,
                admin_id=order.admin_id,
                items=order.items,
                status=order.status,
            )
            for order in orders
        ]
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
