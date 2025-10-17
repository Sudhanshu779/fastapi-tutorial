from fastapi import FastAPI
from .database import engine
from . import models
from .routers import user, post, auth

from .config import settings


models.Base.metadata.create_all(bind=engine)  # To create the models using SQLAlchemy

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}
