from fastapi import FastAPI, APIRouter
from app.routers import blog, user
from app.database import engine
from app import models
import uvicorn


app = FastAPI()
router = APIRouter()
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=4000, reload=True)
