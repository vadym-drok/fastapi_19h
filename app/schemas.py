from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserCreate(UserBase):
    email: EmailStr
    password: str
    name: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
