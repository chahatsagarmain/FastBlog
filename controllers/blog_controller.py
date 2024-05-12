from motor.motor_asyncio import AsyncIOMotorDatabase
from models.models import User
from datetime import datetime
from bson import ObjectId
from models.models import Blog

async def get_all_blogs_controller(db : AsyncIOMotorDatabase):
    blogs_coll = db.get_collection("blogs")
    blogs = await blogs_coll.find({}).to_list(length=None)
    return blogs

async def create_blog_controller(db : AsyncIOMotorDatabase ,blog : Blog):
    users_coll = db.get_collection("users")
    blogs_coll = db.get_collection("blogs")
    
    author = await users_coll.find_one({"id" : ObjectId(blog.author)})
    
    if not author:
        return None 
    
    inserted_blog = await blogs_coll.insert_one(blog)
    
    await users_coll.update_one(
        {"_id": ObjectId(blog.author)},
        {"$addToSet": {"blogs": inserted_blog.inserted_id}}
    )
    
    return inserted_blog.inserted_id