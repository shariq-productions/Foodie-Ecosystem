from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import UserDetailModel
from app.models.cart import CartDetailsModel
from app.models.item import ItemDetailsmModel
from app.models.category import CategoryDetailsModel
from app.models.order import OrderDetailsModel
from app.models.delivery_info import DeliveryInfoDetailsModel
from .config import settings


async def init_db():
    # Beanie uses Motor async client under the hood
    client = AsyncIOMotorClient(settings.database_connection_string)

    # Initialize beanie with the database connection and collection
    await init_beanie(
        database=client.get_database(settings.database_name),
        document_models=[
            UserDetailModel,
            CartDetailsModel,
            ItemDetailsmModel,
            CategoryDetailsModel,
            OrderDetailsModel,
            DeliveryInfoDetailsModel,
        ],
    )
