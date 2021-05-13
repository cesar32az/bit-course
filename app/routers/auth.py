from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app.repositories import auth


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    return auth.login(request, db)

@router.post('/register')
def register():
    return 'register'