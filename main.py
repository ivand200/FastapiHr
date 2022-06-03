from fastapi import FastAPI

from routers.auth import router as router_auth

app = FastAPI()


app.include_router(
    router_auth,
    prefix="/auth",
    tags=["auth"]
)
