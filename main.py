from fastapi import FastAPI
from routes.user_routes import user_router
from routes.blog_routes import blog_router
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from db.connect import connect_to_db
from fastapi.templating import Jinja2Templates
from fastapi.openapi.utils import get_openapi


load_dotenv()
app = FastAPI()

connect_to_db()

app.include_router(user_router,prefix="/api/v1")
app.include_router(blog_router,prefix="/api/v1")

templates = Jinja2Templates(directory="templates")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastBlog",
        version="1.0.0",
        description="API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/docs", response_class=HTMLResponse)
async def custom_swagger_ui(request):
    return templates.TemplateResponse("swagger.html", {"request": request, "openapi_url": "/openapi.json"})
