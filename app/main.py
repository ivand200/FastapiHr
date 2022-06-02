from fastapi import FastAPI

from database.db import engine
from database import models
from .routers import app

models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello Worl"}