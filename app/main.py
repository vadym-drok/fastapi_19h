from fastapi import FastAPI
from .models import Post
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()


DB_USER_NAME = os.getenv('DB_USER_NAME')
DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')

# DATABASE_URL = f'postgresql+psycopg2://{DB_USER_NAME}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

try:
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER_NAME, password=DB_USER_PASSWORD, port=DB_PORT,
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print('DB connect! --- !')
except Exception as error:
    print(f"Err --- {error}")


app = FastAPI(docs_url='/')
# /redoc


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
