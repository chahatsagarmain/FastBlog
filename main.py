from fastapi import FastAPI
from routes.user_routes import user_router
from routes.blog_routes import blog_router
from dotenv import load_dotenv
from db.connect import connect_to_db
import os

load_dotenv()
app = FastAPI()

connect_to_db()

app.include_router(user_router,prefix="/api/v1")
app.include_router(blog_router,prefix="/api/v1")
