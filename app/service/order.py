from fastapi import HTTPException
from app.schema.order import ShowOrderDetails, AddOrderSchema, OrderItemSchema
from app.models.order import OrderDetailsModel
from beanie import PydanticObjectId


async def add_order_details(order: AddOrderSchema) -> ShowOrderDetails:
    order_items = [
        OrderItemSchema(
            item_id=item.item_id,
            item_name=item.item_name,
            quantity=item.quantity,
            price=item.price,
            total_amount=item.total_amount,
        )
        for item in order.items
    ]
    order_detail_docs = OrderDetailsModel(
        user_id=order.user_id,
        admin_id=order.admin_id,
        items=order_items,
        status=order.status,
    )
    try:
        await order_detail_docs.insert()
        return ShowOrderDetails(d=order_detail_docs.id)
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
