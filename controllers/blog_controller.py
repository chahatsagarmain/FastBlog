from motor.motor_asyncio import AsyncIOMotorDatabase
from models.models import Comment
from models.request_models import UpdateBlog
from datetime import datetime
from bson import ObjectId
from models.models import Blog

async def get_all_blogs_controller(db : AsyncIOMotorDatabase):
    blogs_coll = db.get_collection("blogs")
    blogs = await blogs_coll.find({}).to_list(length=None)
    return blogs

async def get_blog_controller_by_id(db : AsyncIOMotorDatabase , id : str):
    blogs_coll = db.get_collection("blogs")
    blog = await blogs_coll.find_one(filter={"_id" : ObjectId(id)})
    return blog

async def create_blog_controller(db : AsyncIOMotorDatabase ,blog : Blog):
    users_coll = db.get_collection("users")
    blogs_coll = db.get_collection("blogs")
    
    blog['created_on'] = datetime.now()
    
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

async def update_blog_like_controller(db : AsyncIOMotorDatabase , id : str):
    blog_coll = db.get_collection("blogs")
    
    update_result = await blog_coll.update_one(filter={"_id" : ObjectId(id)},update={"$inc" : {"likes" : 1}})
    
    if update_result.matched_count == 0:
        return None
    
    return update_result

async def update_blog_dislike_controller(db : AsyncIOMotorDatabase , id : str):
    blog_coll = db.get_collection("blogs")
    
    update_result = await blog_coll.update_one(filter={"_id" : ObjectId(id)},update={"$inc" : {"dislikes" : 1}})
    
    if update_result.matched_count == 0:
        return None
    
    return update_result


async def update_blog_unlike_controller(db : AsyncIOMotorDatabase , id : str):
    blog_coll = db.get_collection("blogs")
    
    update_result = await blog_coll.update_one(filter={"_id" : ObjectId(id)},update={"$inc" : {"likes" : -1}})
    
    if update_result.matched_count == 0:
        return None
    
    return update_result


async def update_blog_undislike_controller(db : AsyncIOMotorDatabase , id : str):
    blog_coll = db.get_collection("blogs")
    
    update_result = await blog_coll.update_one(filter={"_id" : ObjectId(id)},update={"$inc" : {"dislikes" : -1}})
    
    if update_result.matched_count == 0:
        return None
    
    return update_result

async def delete_blog_controller(db : AsyncIOMotorDatabase , id : str):
    blog_coll = db.get_collection("blogs")
    
    delete_result = await blog_coll.delete_one(filter={"_id" : ObjectId(id)})
    
    if delete_result.deleted_count == 0:
        return 0
    
    return True


async def get_all_comments_controller(db : AsyncIOMotorDatabase,id : str):
    blogs_coll = db.get_collection("blogs")
    blog = await blogs_coll.find_one(filter={"_id" : ObjectId(id)})
    comments_id = Blog(**blog).comments
    comments_coll = db.get_collection("comments")
    comments = [Comment(**(await comments_coll.find_one(filter={"_id" : ObjectId(comment_id)}))).model_dump(mode='json') for comment_id in comments_id]
    return comments


async def create_comment_controller(db : AsyncIOMotorDatabase,comment : Comment,id : str):
    blogs_coll = db.get_collection("blogs")
    comments_coll = db.get_collection("comments")
    
    blog_found = await blogs_coll.find_one(filter={"_id" : ObjectId(id)})
    
    if not blog_found:
        return None
    
    print(blog_found)
    
    comment_dict = comment.model_dump()
    comment_dict["created_on"] = datetime.now()
    comment_dict["parent_blog"] = ObjectId(id)
    
    print(comment_dict)
    
    inserted_comment = await comments_coll.insert_one(comment_dict)
    print(1)
    if not inserted_comment.inserted_id:
        return None 
    
    updated_blog = await blogs_coll.update_one(filter={"_id" : ObjectId(id)}
                                               ,update={"$addToSet" : {"comments" : inserted_comment.inserted_id}})
    print(1)
    if updated_blog.modified_count == 0:
        return None 
    print(2)
     
    return inserted_comment.inserted_id
    