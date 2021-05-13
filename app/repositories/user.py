from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.hashing import Hash


def create(user: schemas.User, db: Session):
    hashedPass = Hash.hashPassword(user.password)
    new_user = models.User(
        name=user.name, email=user.email, password=hashedPass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} not found")
    return user
