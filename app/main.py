from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session



from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/')
# /redoc



from pydantic import BaseModel
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

from .settings import DB_HOST, DB_NAME, DB_USER_NAME, DB_USER_PASSWORD, DB_PORT
try:
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER_NAME, password=DB_USER_PASSWORD, port=DB_PORT,
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print('DB connect! --- !')
except Exception as error:
    print(f"Err --- {error}")



@app.get('/sqlalchemy')
def test_post(db: Session = Depends(get_db)):
        return {'status': 'done!'}


@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post('/posts', status_code=201)
def create_post(post_data: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post_data.title, post_data.content, post_data.published)
    )
    new_post = cursor.fetchall()
    conn.commit()
    return {
        'data': new_post
    }
