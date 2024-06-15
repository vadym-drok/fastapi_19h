from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .models import Post


from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/')
# /redoc


from pydantic import BaseModel
class PostForm(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()

    return {'data': posts}

@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return {'data': post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: PostForm, db: Session = Depends(get_db)):
    new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'data': new_post}


@app.delete('/posts/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db.delete(post)
    db.commit()

    return {'data': post}


@app.put('/posts/{id}')
def update_post(id: int, post: PostForm, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    updated_post = post_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post_query.update(post.dict())

    db.commit()

    return {'data': post_query.first()}
