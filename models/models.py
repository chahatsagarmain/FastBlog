from pydantic import BaseModel , BeforeValidator , Field
from datetime import datetime
from typing import List, Optional , Annotated 

PyObjectId = Annotated[str, BeforeValidator(str)]

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: str
    password: str
    created_on: Optional[datetime] = None
    blogs: Optional[List[PyObjectId]] = []

class Blog(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    content: str
    likes: int = 0
    dislikes: int = 0
    author: str
    created_on: Optional[datetime] = None
    comments: List[PyObjectId] = []

class Comment(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    author: Optional[PyObjectId]
    text: str
    likes: int = 0
    dislikes: int = 0
    created_on: Optional[datetime] = None
    parent_blog : Optional[PyObjectId] = None
    parent_comment : Optional[PyObjectId] = None
