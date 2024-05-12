from motor.motor_asyncio import AsyncIOMotorDatabase
from models.models import User
from models.request_models import UpdateUser
from datetime import datetime
from bson import ObjectId

async def create_user_controller(db : AsyncIOMotorDatabase,user : User):

    user_coll = db.get_collection("users")
    user_doc = user.model_dump()
    user_doc["created_on"] = datetime.now()
    user_found = await  user_coll.find_one(filter={"$or" : [{"username" : user_doc.get("username"),
                                                            "email" : user_doc.get("email")}]})
    if user_found:
        return None
    inserted_user = await user_coll.insert_one(user_doc)
    return inserted_user.inserted_id
    
async def get_all_users(db :AsyncIOMotorDatabase):
    
    user_coll = db.get_collection("users")
    users = await user_coll.find().to_list(length=None)
    return users

async def update_user_controller(db : AsyncIOMotorDatabase , update_user : UpdateUser,id : str):
    users_coll = db.get_collection("users")
    user_found = await users_coll.find_one(filter={"_id" : ObjectId(id)})
    if not user_found:
        return None 
    user = User(**user_found).model_dump()
    update_data = update_user.model_dump()
    for key, value in user.items():
        if key not in update_data:
            update_data[key] = value
    updated_user = await users_coll.update_one(filter={"_id" : ObjectId(id)},update={"$set" : update_data})
    return updated_user.acknowledged

async def delete_user_controller(db: AsyncIOMotorDatabase,id : str):
    user_coll = db.get_collection("users")
    deleted_user = await user_coll.delete_one(filter={"_id" : ObjectId(id)})
    return deleted_user.acknowledged
    