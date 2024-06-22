from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .models import Post, User
from .schemas import PostCreate, PostResponse, UserCreate, UserResponse
from . import models
from .database import engine, get_db
from .utils import hashed

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/')
# /redoc


@app.get('/posts', response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()

    return posts


@app.get('/posts/{id}', response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.delete('/posts/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db.delete(post)
    db.commit()

    return post


@app.put('/posts/{id}')
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), response_model=PostResponse):
    post_query = db.query(Post).filter(Post.id == id)
    updated_post = post_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post_query.update(post.dict())

    db.commit()

    return post_query.first()


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.password = hashed(user.password)

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/users/{id}', response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
