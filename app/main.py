from fastapi import FastAPI
from . import models
from app.database import engine
from app.routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/')
# /redoc


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
