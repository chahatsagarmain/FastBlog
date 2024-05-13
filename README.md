# FastBlog
FastBlog is a REST API developed with FastApi and MongoDB as its database . I built this for one of the assignements under one day . Feel free to debug and make improvements !
## Setting up locally 
Clone this repository locally by entering the following command in terminal :-

    git clone https://github.com/chahatsagarmain/FastBlog.git

Change current directory to FastBlog:-

    cd FastBlog

Run the application on port 8000:

    fastapi dev main.py 

 
## Data Models 
### User Model

    class User(BaseModel):
        id: Optional[str] = Field(alias="_id", default=None)
        username: str
        email: str
        password: str
        created_on: Optional[datetime] = None
        blogs: Optional[List[str]] = []
-   **id**: Unique identifier for the user.
-   **username**: Username of the user.
-   **email**: Email address of the user.
-   **password**: Password of the user.
-   **created_on**: Timestamp indicating when the user was created.
-   **blogs**: List of blog IDs associated with the user.
### Blog Model 

    class Blog(BaseModel):
        id: Optional[str] = Field(alias="_id", default=None)
        title: str
        content: str
        likes: int = 0
        dislikes: int = 0
        author: str
        created_on: Optional[datetime] = None
        comments: List[str] = []
-   **id**: Unique identifier for the blog.
-   **title**: Title of the blog.
-   **content**: Content of the blog.
-   **likes**: Number of likes the blog has received.
-   **dislikes**: Number of dislikes the blog has received.
-   **author**: Username of the user who authored the blog.
-   **created_on**: Timestamp indicating when the blog was created.
-   **comments**: List of comment IDs associated with the blog.
### Comment Model 

    class Comment(BaseModel):
        id: Optional[str] = Field(alias="_id", default=None)
        author: Optional[str]
        text: str
        likes: int = 0
        dislikes: int = 0
        created_on: Optional[datetime] = None
        parent_blog: Optional[str] = None
        parent_comment: Optional[str] = None
-   **id**: Unique identifier for the comment.
-   **author**: Username of the user who posted the comment.
-   **text**: Text content of the comment.
-   **likes**: Number of likes the comment has received.
-   **dislikes**: Number of dislikes the comment has received.
-   **created_on**: Timestamp indicating when the comment was created.
-   **parent_blog**: ID of the parent blog to which the comment belongs.
-   **parent_comment**: ID of the parent comment to which the comment belongs.
## API Endpoints
Documentation for API endpoints and schemas can be accessed by accessing route

    http://localhost:8000/docs
