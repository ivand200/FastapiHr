from fastapi import FastAPI

from routers.auth import router as router_auth
from routers.clients import router as router_clients
from db import Base, engine
from models import models_db

app = FastAPI()


models_db.Base.metadata.create_all(bind=engine)

app.include_router(
    router_auth,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    router_clients,
    prefix="/clients",
    tags=["clients"]
)
