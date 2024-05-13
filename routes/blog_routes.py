from fastapi import APIRouter
from db.connect import connect_to_db
from controllers import blog_controller
from models.models import Blog , Comment
from fastapi.responses import JSONResponse
from bson import json_util
from models.request_models import UpdateBlog

blog_router = APIRouter()
client, db = connect_to_db()

@blog_router.get("/blogs")
async def get_all_blogs():
    global db
    blogs = await blog_controller.get_all_blogs_controller(db)
    blogs_json = [Blog(**blog).model_dump(mode='json') for blog in blogs]
    return JSONResponse(content={"data" : blogs_json},status_code=200)

@blog_router.get("/blog/{id}")
async def get_blog(id : str):
    global db
    blog = await blog_controller.get_blog_controller_by_id(db,id)
    blog_json = Blog(**blog).model_dump(mode = "json")
    return JSONResponse(content={"data" : blog_json},status_code=200)


@blog_router.post("/blog")
async def create_blog(blog : Blog):
    global db 
    try:
        inserted_blog = await blog_controller.create_blog_controller(db,blog)
        if not inserted_blog:
            return JSONResponse(content={"message" : "blog not inserted"},status_code=400)
        return JSONResponse(content={"message" : "blog inserted" , "data" : json_util.dumps(inserted_blog)})
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

@blog_router.put("/blog/{id}")
async def update_blog(blog : UpdateBlog,id : str):
    global db
    try:
        update_blog = await blog_controller.update_blog_controller(db,blog,id)
        if not update_blog:
            return JSONResponse(content={"message" : "no updated"},status_code=400)
        return JSONResponse(content={"message" : "blog updated" , "data" : Blog(**update_blog).model_dump(mode='json')})
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)
    

@blog_router.put("/blog/like/{id}")
async def update_blog_like(id : str):
    try:
        updated_blog = await blog_controller.update_blog_like_controller(db, id)
        
        if not updated_blog:
            return JSONResponse(content={"message" : "no updated"},status_code=400)
        
        return JSONResponse(content={"message" : "blog updated"})
    
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

@blog_router.put("/blog/unlike/{id}")
async def update_blog_like(id : str):
    try:
        updated_blog = await blog_controller.update_blog_unlike_controller(db, id)
        
        if not updated_blog:
            return JSONResponse(content={"message" : "no updated"},status_code=400)
        
        return JSONResponse(content={"message" : "blog updated"})
    
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)
    
    
@blog_router.put("/blog/dislike/{id}")
async def update_blog_like(id : str):
    try:
        updated_blog = await blog_controller.update_blog_dislike_controller(db, id)
        
        if not updated_blog:
            return JSONResponse(content={"message" : "no updated"},status_code=400)
        
        return JSONResponse(content={"message" : "blog updated"})
    
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

@blog_router.put("/blog/undislike/{id}")
async def update_blog_like(id : str):
    try:
        updated_blog = await blog_controller.update_blog_undislike_controller(db, id)
        
        if not updated_blog:
            return JSONResponse(content={"message" : "no updated"},status_code=400)
        
        return JSONResponse(content={"message" : "blog updated"})
    
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)
    
@blog_router.delete("/blog/{id}")
async def delete_blog(id : str):
    try:
        deleted_blog = await blog_controller.delete_blog_controller(db, id)
        
        if not deleted_blog:
            return JSONResponse(content={"message" : "no deleted"},status_code=400)
        
        return JSONResponse(content={"message" : "blog deleted"})
    
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

@blog_router.get("/blog/{id}/comments")
async def get_comments(id : str):
    global db
    commnets = await blog_controller.get_all_comments_controller(db,id)
 
    return JSONResponse(content={"data" : commnets},status_code=200)

@blog_router.post("/blog/{id}/comment")
async def create_commnet(id : str, commnet : Comment):
    try:
        inserted_comment = await blog_controller.create_comment_controller(db,commnet,id)

        if not inserted_comment:
            return JSONResponse(content={"message" : "comment not inserted" },status_code=400)
        return JSONResponse(content={"message" : "comment inserted","data" : json_util.dumps(inserted_comment)},status_code=200)
        
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

#delete update like dislike comment 