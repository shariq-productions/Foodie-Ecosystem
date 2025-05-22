from app.dependencies.auth import get_current_user
from fastapi import APIRouter, Depends
from app.routes.user import userRouter
from app.routes.cart import cartRouter
from app.routes.delivery_info import deliveryInfoRouter
from app.routes.item import itemRouter
from app.routes.order import orderRouter
from app.routes.category import categoryRouter

router = APIRouter()

router.include_router(userRouter, prefix="/user", tags=["user"])
router.include_router(
    cartRouter, prefix="/cart", tags=["cart"], dependencies=[Depends(get_current_user)]
)
router.include_router(
    deliveryInfoRouter,
    prefix="/deliveryInfo",
    tags=["deliveryInfo"],
    dependencies=[Depends(get_current_user)],
)
router.include_router(
    itemRouter, prefix="/item", tags=["item"], dependencies=[Depends(get_current_user)]
)
router.include_router(
    orderRouter,
    prefix="/order",
    tags=["order"],
    dependencies=[Depends(get_current_user)],
)
router.include_router(
    categoryRouter,
    prefix="/category",
    tags=["category"],
    dependencies=[Depends(get_current_user)],
)
