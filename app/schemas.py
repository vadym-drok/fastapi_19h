from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr, conint


# User
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    name: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostListResponse(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[Union[str, int]] = None


# Votes
class VoteAddDelete(BaseModel):
    post_id: int
    dir: conint(le=1)
