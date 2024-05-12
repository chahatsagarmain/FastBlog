from pydantic import BaseModel
from typing import Optional , List
from datetime import datetime
from models.models import Blog

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    created_on: Optional[datetime] = None
    blogs: Optional[List["Blog"]] = None
