from motor.motor_asyncio import AsyncIOMotorDatabase
from models.models import User
from datetime import datetime
from bson import ObjectId

async def get_all_blogs_controller(db : AsyncIOMotorDatabase):
    blogs_coll = db.get_collection("blogs")
    blogs = await blogs_coll.find({}).to_list(length=None)
    return blogs