from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas, models

from app.repositories import blog

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db)):
    blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(new_blog: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create_blog(new_blog, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def get_blog(id: int, db: Session = Depends(get_db)):
    return blog.get_one(id, db)


@router.put('/{id}', status_code=200)
def update_blog(id: int, new_blog: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update_blog(id, new_blog, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id, db: Session = Depends(get_db)):
    return blog.delete_one(id, db)
