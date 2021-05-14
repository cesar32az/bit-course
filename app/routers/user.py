from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.repositories import user
router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(new_user: schemas.User, db: Session = Depends(get_db)):
    return user.create(new_user, db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get(id, db)