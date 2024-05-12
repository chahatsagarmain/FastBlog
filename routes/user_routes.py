from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.models import User
from models.request_models import UpdateUser
from db.connect import connect_to_db
from controllers import user_controller
from bson import json_util

user_router = APIRouter()
client, db = connect_to_db()

@user_router.get("/users")
async def get_users():
    try:
        users = await user_controller.get_all_users(db)
        user_data = [User(**user).model_dump_json() for user in users]
        return JSONResponse(content={"data": user_data}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

@user_router.post("/user")
async def create_user(user: User):
    try:
        inserted_id = await user_controller.create_user_controller(db, user)
        if not inserted_id:
            return JSONResponse(content={"message": "User already present"}, status_code=400)
        return JSONResponse(content={"message": "User inserted successfully", "id": json_util.dumps(inserted_id)}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

@user_router.put("/user/{id}")
async def update_user(update_user: UpdateUser, id: str):
    try:
        updated_user = await user_controller.update_user_controller(db, update_user, id)
        if not updated_user:
            return JSONResponse(content={"detail": "User not found or not updated"}, status_code=404)
        return JSONResponse(content={"message": "User updated successfully", "data": json_util.dumps(updated_user)}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

@user_router.delete("/user/{id}")
async def delete_user(id: str):
    try:
        deleted_user = await user_controller.delete_user_controller(db, id)
        if not deleted_user:
            return JSONResponse(content={"detail": "User not found or not deleted"}, status_code=404)
        return JSONResponse(content={"message": "Deleted user", "data": deleted_user}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)
