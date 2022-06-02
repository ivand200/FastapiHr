from pyexpat import model
from fastapi import APIRouter, Depends, HTTPException, Security, Header
from sqlalchemy.orm import Session
from database import models, schemas
from database.db import get_db
from fastapi.responses import JSONResponse

import bcrypt

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
    hashed_password = bcrypt.hashpw(user.password.encode("utf8"), bcrypt.gensalt())
    db_user = models.AbstractUser(
        username=user.username, email=user.email, password=hashed_password
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


@router_auth.post("/managers/signup/", response_model=schemas.User, status_code=201)
async def create_manager(manager: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a manager
    """
    check_email = (
        db.query(models.AbstractUser)
        .filter(models.AbstractUser.email == manager.email)
        .first()
    )
    check_username = (
        db.query(models.AbstractUser)
        .filter(models.AbstractUser.username == manager.username)
        .first()
    )
    if check_email or check_username:
        raise HTTPException(status_code=400, detail="Email or username already exists.")
    hashed_password = bcrypt.hashpw(manager.password.encode("utf8"), bcrypt.gensalt())
    db_manager = models.AbstractUser(
        username=manager.username, email=manager.email, password=hashed_password
    )
    new_manager = models.Manager(users=db_manager)
    db.add(db_manager)
    db.add(new_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager


@router_auth.delete("/managers/{id}/", status_code=200)
async def delete_manager(id: int, db: Session = Depends(get_db)):
    """
    Deelete manager by id
    """
    db_manager = (
        db.query(models.AbstractUser).filter(models.AbstractUser.id == id).first()
    )
    if not db_manager:
        raise HTTPException(status_code=400, detail="Manager does not exist.")
    db.delete(db_manager)
    db.commit()
    return f"Manager {db_manager} was deleted."
