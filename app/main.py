from fastapi import FastAPI, Depends, status
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


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: PostForm, db: Session = Depends(get_db)):
    new_post = Post(
        title=post.title,
        content=post.content,
        published=post.published,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'data': new_post}
