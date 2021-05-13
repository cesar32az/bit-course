from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.hashing import Hash
from app import schemas, models

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    hashedPass = Hash.hashPassword(user.password)
    new_user = models.User(
        name=user.name, email=user.email, password=hashedPass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} not found")
    return user
