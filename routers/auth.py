# TODO: Auth with pyjwt
# TODO: login api for clients and managers
# TODO: permissions for managers and clients

from fastapi import APIRouter, Depends, HTTPException, Security, Header, status
from sqlalchemy.orm import Session
from models import models_db
from schemas import auth
from db import get_db
from fastapi.responses import JSONResponse

import bcrypt

router = APIRouter()


@router.get("/test/", status_code=201)
async def auth_users():
    return "Hello"


@router.post("/clients/", response_model=auth.User, status_code=status.HTTP_201_CREATED)
async def create_client(user: auth.UserCreate, db: Session = Depends(get_db)):
    """
    Create a client
    """
    check_email = (
        db.query(models_db.AbstractUser)
        .filter(models_db.AbstractUser.email == user.email)
        .first()
    )
    check_username = (
        db.query(models_db.AbstractUser)
        .filter(models_db.AbstractUser.username == user.username)
        .first()
    )
    if check_email or check_username:
        raise HTTPException(status_code=400, detail="Email or username already exists.")
    hashed_password = bcrypt.hashpw(user.password.encode("utf8"), bcrypt.gensalt())
    db_user = models_db.AbstractUser(
        username=user.username, email=user.email, password=hashed_password
    )
    new_client = models_db.Client(users=db_user)
    db.add(db_user)
    db.add(new_client)
    db.commit()
    db.refresh(db_user)
    # serializer = schemas.User(**new_user)
    return db_user


@router.delete("/clients/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(id: int, db: Session = Depends(get_db)):
    """
    Delete client by id
    """
    db_user = db.query(models_db.AbstractUser).filter(models_db.AbstractUser.id == id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist.")
    db.delete(db_user)
    db.commit()
    return f"Client {db_user}, was deleted."


@router.put("/clients/{id}", response_model=auth.User, status_code=200)
async def update_client(id: int, db: Session = Depends(get_db)):
    """
    Update existing client
    """


@router.post("/managers/signup/", response_model=auth.User, status_code=status.HTTP_201_CREATED)
async def create_manager(manager: auth.UserCreate, db: Session = Depends(get_db)):
    """
    Create a manager
    """
    check_email = (
        db.query(models_db.AbstractUser)
        .filter(models_db.AbstractUser.email == manager.email)
        .first()
    )
    check_username = (
        db.query(models_db.AbstractUser)
        .filter(models_db.AbstractUser.username == manager.username)
        .first()
    )
    if check_email or check_username:
        raise HTTPException(status_code=400, detail="Email or username already exists.")
    hashed_password = bcrypt.hashpw(manager.password.encode("utf8"), bcrypt.gensalt())
    db_manager = models_db.AbstractUser(
        username=manager.username, email=manager.email, password=hashed_password
    )
    new_manager = models_db.Manager(users=db_manager)
    db.add(db_manager)
    db.add(new_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager


@router.delete("/managers/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_manager(id: int, db: Session = Depends(get_db)):
    """
    Deelete manager by id
    """
    db_manager = (
        db.query(models_db.AbstractUser).filter(models_db.AbstractUser.id == id).first()
    )
    if not db_manager:
        raise HTTPException(status_code=400, detail="Manager does not exist.")
    db.delete(db_manager)
    db.commit()
    return f"Manager {db_manager} was deleted."
