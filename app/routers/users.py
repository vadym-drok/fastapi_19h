from app.models import User
from app.schemas import UserCreate, UserResponse
from app.database import get_db
from sqlalchemy.orm import Session

from fastapi import Depends, status, HTTPException, APIRouter

from app.utils import hashed


router = APIRouter(
    prefix='/users'
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.password = hashed(user.password)

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
