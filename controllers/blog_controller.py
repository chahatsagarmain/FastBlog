from motor.motor_asyncio import AsyncIOMotorDatabase
from models.models import User
from models.request_models import UpdateBlog
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
    
    author = await users_coll.find_one({"_id" : ObjectId(blog.author)})

    if not author:
        return None 
    
    inserted_blog = await blogs_coll.insert_one(blog.model_dump())
    print(inserted_blog)
    print(inserted_blog.inserted_id)
    
    updated_user = await users_coll.update_one(
        {"_id": ObjectId(blog.author)},
        {"$addToSet": {"blogs": inserted_blog.inserted_id}}
    )
    print(updated_user)
    print(inserted_blog)
    
    return inserted_blog.inserted_id

async def update_blog_controller(db : AsyncIOMotorDatabase , update_blog : UpdateBlog,id : str):
    blog_coll = db.get_collection("blogs")
    update_blog_dict = update_blog.model_dump(exclude_unset=True)
    print(update_blog_dict)
    update_result = await blog_coll.update_one(filter={"_id" : ObjectId(id)},update={"$set" : update_blog_dict})
    
    if update_result.modified_count == 0:
        return None 
    
    updated_blog = await blog_coll.find_one(filter={"_id" : ObjectId(id)})
    
    return updated_blog
    