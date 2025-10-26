from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, auth
from ..utils import get_db

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/register', response_model=schemas.Token)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    user = models.User(email=user_in.email, hashed_password=auth.get_password_hash(user_in.password), is_admin=user_in.is_admin)
    db.add(user); db.commit(); db.refresh(user)
    token = auth.create_access_token({'sub': user.id})
    return {'access_token': token}

@router.post('/token', response_model=schemas.Token)
def login(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect credentials')
    token = auth.create_access_token({'sub': user.id})
    return {'access_token': token}
