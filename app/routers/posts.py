from typing import List
from app.models import Post
from app.schemas import PostCreate, PostResponse
from app.database import get_db
from sqlalchemy.orm import Session

from fastapi import Depends, status, HTTPException, APIRouter


router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)


@router.get('/', response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()

    return posts


@router.get('/{id}', response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db.delete(post)
    db.commit()

    return post


@router.put('/{id}', response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    updated_post = post_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post_query.update(post.dict())

    db.commit()

    return post_query.first()