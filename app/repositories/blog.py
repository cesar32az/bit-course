from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(blog: schemas.Blog, db: Session):
    new_blog = models.Blog(
        title=blog.title, body=blog.body, published=blog.published, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_one(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Blog with the id {id} not found"} #remember import Response
    return blog


def delete_blog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Blog deleted'}


def update_blog(id: int, new_blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found")
    blog.update(new_blog)
    db.commit()
    return {'detail': 'Blog updated'}
