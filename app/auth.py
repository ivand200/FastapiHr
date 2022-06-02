# TODO: create client and delete client properly
# TODO: with tests
# TODO: checking existing clients
# TODO: with all excetions (HTTP), status_code
# TODO: hash password
# TODO: check with blacke and flake8

from fastapi import APIRouter, Depends, HTTPException, Security, Header
from sqlalchemy.orm import Session
from database import models, schemas
from database.db import get_db
from fastapi.responses import JSONResponse

router_auth = APIRouter()


@router_auth.get("/test/", status_code=201)
async def auth_users():
    return "Hello"


@router_auth.post("/clients/", response_model=schemas.User, status_code=201)
async def create_client(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a client
    """
    check_email = (
        db.query(models.AbstractUser)
        .filter(models.AbstractUser.email == user.email)
        .first()
    )
    check_username = (
        db.query(models.AbstractUser)
        .filter(models.AbstractUser.username == user.username)
        .first()
    )
    if check_email or check_username:
        raise HTTPException(status_code=400, detail="Email or username already exists.")
    db_user = models.AbstractUser(
        username=user.username, email=user.email, password=user.password
    )
    new_client = models.Client(users=db_user)
    db.add(db_user)
    db.add(new_client)
    db.commit()
    db.refresh(db_user)
    # serializer = schemas.User(**new_user)
    return db_user


@router_auth.delete("/clients/{id}/", status_code=200)
async def delete_client(id: int, db: Session = Depends(get_db)):
    """
    Delete client by id
    """
    db_user = db.query(models.AbstractUser).filter(models.AbstractUser.id == id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist.")
    db.delete(db_user)
    db.commit()
    return f"Client {db_user}, was deleted."


@router_auth.put("/clients/{id}", response_model=schemas.User, status_code=200)
async def update_client(id: int, db: Session = Depends(get_db)):
    """
    Update existing client
    """
