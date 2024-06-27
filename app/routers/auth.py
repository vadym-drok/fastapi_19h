from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils import verify
from app.oauth2 import create_access_token


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()  # username - email

    if user is None or not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    return {
        "access_token": create_access_token(data={'user_id': user.id}),
        'token_type': 'bearer',
    }
