from fastapi import FastAPI
from .auth import router_auth


app = FastAPI()

app.include_router(
    router_auth,
    prefix="/auth",
    tags=["auth"]
)