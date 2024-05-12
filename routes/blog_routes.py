from fastapi import APIRouter
from db.connect import connect_to_db
from controllers import blog_controller
from models.models import Blog
from fastapi.responses import JSONResponse
from bson import json_util

blog_router = APIRouter()
client, db = connect_to_db()

@blog_router.get("/blogs")
async def get_all_blogs():
    global db
    blogs = await blog_controller.get_all_blogs_controller(db)
    blogs_json = [Blog(**blog).model_dump_json() for blog in blogs]
    return JSONResponse(content={"data" : blogs_json},status_code=200)

@blog_router.post("/blog")
async def create_blog(blog : Blog):
    global db 
    try:
        inserted_blog = await blog_controller.create_blog_controller(db,blog)
        if not inserted_blog:
            return JSONResponse(content={"message" : "blog not inserted"},status_code=400)
        return JSONResponse(content={"message" : "blog inserted" , "data" : json_util.dumps(inserted_blog)})
    except Exception as e:
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)
    