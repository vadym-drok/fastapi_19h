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


my_posts = [{'title': 't1', 'content': 'c2', 'id': 1}]

@app.get("/test")
async def root():
    return {"message": "Hello World"}

@app.post('/test_post')
def test_post(post_data: Post):
    print(post_data)
    return {
        'test': 'Done POST!'
    }