from app.models.user import UserDetailModel
from fastapi import HTTPException
from pydantic import EmailStr
from app.schema.user import ShowUserDetails, ChangePasswordSchema
from app.models.user import UserType
import bcrypt
from pymongo.errors import DuplicateKeyError
from beanie import PydanticObjectId
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def add_user_details(
    email: EmailStr, password: str, name: str, user_type: UserType
) -> ShowUserDetails:

    try:
        hashed_password = pwd_context.hash(password)

        user_detail = UserDetailModel(
            email=email, password=hashed_password, user_type=user_type, name=name
        )
        await user_detail.insert()
        return user_detail

    except DuplicateKeyError:
        print(f"Error: Email '{email}' already exists.")
        raise HTTPException(
            status_code=400, detail=f"Error: Email '{email}' already exists."
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=404, detail=f"An error occurred: {str(e)}")


async def delete_user_by_id(user_id: PydanticObjectId):

    try:
        user_obj = await UserDetailModel.find_one(UserDetailModel.id == user_id)
        if not user_obj:
            raise HTTPException(status_code=404, detail="User not found")
        await user_obj.delete()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "User deleted"}


async def update_user_password_by_id(
    user_id: PydanticObjectId, data: ChangePasswordSchema
):

    try:
        user_obj = await UserDetailModel.find_one(UserDetailModel.id == user_id)
        if not user_obj:
            raise HTTPException(status_code=404, detail="User not found")
        hashed_password = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Update the user's password
        user_obj.password = hashed_password
        await user_obj.save()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "User password updated"}


async def get_all_users_list():
    users = await UserDetailModel.find_all().to_list()
    return {"users": users}


async def get_user_by_id(user_id: PydanticObjectId):
    user_obj = await UserDetailModel.find_one(UserDetailModel.id == user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")

    return user_obj
