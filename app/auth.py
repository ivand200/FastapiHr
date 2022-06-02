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
    db_user = models.AbstractUser(username=user.username, email=user.email, password=user.password)
    new_client = models.Client(users=db_user)
    db.add(db_user)
    db.add(new_client)
    db.commit()
    db.refresh(db_user)
    # serializer = schemas.User(**new_user)
    return db_user


@router_auth.delete("/clients/{id}", status_code=200)
async def delete_client(id: int, db: Session = Depends(get_db)):
    """
    Delete client by id
    """
    db_user = db.query(models.AbstractUser).filter(models.AbstractUser.id==id).first()
    db.delete(db_user)
    db.commit()
    return f"Client with id: {id}, was deleted "


@router_auth.put("/clients/{id}", response_model=schemas.User, status_code=200)
async def update_client(id: int, db: Session = Depends(get_db)):
    """
    Update existing client
    """
    pass