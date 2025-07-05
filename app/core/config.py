from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    database_connection_string: str = os.environ.get("DATABASE_CONNECTION_STRING")
    database_name: str = os.environ.get("DATABASE_NAME")
    jwt_secret_key: str = os.environ.get("JWT_SECRET_KEY")
    access_token_expire_minutes: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    algorithm: str = os.environ.get("ALGORITHM")
    stripe_publishable_key: str = os.environ.get("STRIPE_PUBLISHABLE_KEY")
    stripe_app_name :str = os.environ.get("STRIPE_APP_NAME")
    stripe_app_version: str = os.environ.get("STRIPE_APP_VERSION")  
    stripe_app_url: str = os.environ.get("STRIPE_APP_URL")
    stripe_api_version: str = os.environ.get("STRIPE_API_VERSION")
    stripe_api_key: str = os.environ.get("STRIPE_API_KEY")

settings = Settings()
