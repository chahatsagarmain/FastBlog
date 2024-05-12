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
    blogs: Optional[List["Blog"]] = []

class Blog(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    content: str
    likes: int = 0
    dislikes: int = 0
    author: User
    created_on: Optional[datetime] = None
    comments: List["Comment"] = []

class Comment(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    author: Optional[User] = None
    text: str
    likes: int = 0
    dislikes: int = 0
    created_on: Optional[datetime] = None
    parent_blog : Optional["Blog"] = None
    parent_comment : Optional["Comment"] = None
