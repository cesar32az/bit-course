from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'Julio R'}}


@app.get('/blog')
def blogs(limit: int = 10, published: bool = True, sort: Optional[str] = None):

    if published:
        # only get published blogs defined by the limit
        return {'data': f'{limit} published blogs from the db'}
    else:
        # only get blogs defined by the limit
        return {'data': f'{limit} blogs from the db'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int, limit=10):
    # fetch comments of blog with id = id
    return {'data': {'limit': limit, 'comments': ['c1', 'c2']}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f'Blog is created with title as {blog.title}'}


if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=4000, reload=True)
