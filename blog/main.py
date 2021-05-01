from fastapi import FastAPI, Depends, status, Response, HTTPException
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
import uvicorn
from . import schemas
from . import models

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=blog.title, body=blog.body, published=blog.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Blog with the id {id} not found"}
    return blog


@app.put('/blog/{id}', status_code=200)
def update_blog(id: int, new_blog: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found")
    blog.update(new_blog)
    db.commit()
    return {'detail': 'Blog updated'}


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Blog deleted'}


if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=4000, reload=True)
