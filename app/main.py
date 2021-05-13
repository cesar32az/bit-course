from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import blog, user, auth
from app.database import engine
from app import models
import uvicorn
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

models.Base.metadata.create_all(engine)

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=4000, reload=True)
