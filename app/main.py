from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from . import models
# from app.database import engine
from app.routers import posts, users, auth, votes

# Auto-create Tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/')
# /redoc

origins = [
    "*"  # for all
    # "https://www.google.com/",
    # "https://www.pinterest.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
