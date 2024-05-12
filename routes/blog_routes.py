from fastapi import APIRouter
from db.connect import connect_to_db
from controllers import blog_controller
from models.models import Blog
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

blog_router = APIRouter()
client, db = connect_to_db()

@blog_router.get("/blogs")
async def get_all_blogs():
    global db
    blogs = await blog_controller.get_all_blogs_controller(db)
    blogs_json = [Blog(**blog).model_dump_json() for blog in blogs]
    return R    