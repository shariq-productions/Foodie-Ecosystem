from app.models.user import UserDetailModel
from fastapi import HTTPException
from pydantic import EmailStr
from app.schema.user import ShowUserDetails
import bcrypt
from pymongo.errors import DuplicateKeyError


async def add_user_details(email: EmailStr, password: str) -> ShowUserDetails:
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )

    user_detail = UserDetailModel(email=email, password=hashed_password)

    try:
        await user_detail.insert()
        return user_detail

    except DuplicateKeyError:
        print(f"Error: Email '{email}' already exists.")
        raise HTTPException(
            status_code=400, detail=f"Error: Email '{email}' already exists."
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
