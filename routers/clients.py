from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Security,
    Header,
    status,
    Body,
    Form,
    Request,
    Query,
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from typing import List, Union
import json

from models import models_db
from schemas import auth, tags
from db import get_db

router = APIRouter()

# @router.get("/test")
# def add_tags_to_client(name: str = Body(...), age: int = Body(...)):
#     return {"name": name, "age": age}


@router.post("/client/{client_id}", response_model=tags.ClientBase, status_code=status.HTTP_201_CREATED)
def add_tags_to_client(
    client_id: int, tags_id: tags.TagsAdd, db: Session = Depends(get_db)
):
    """
    Add tags to client
    """
    client_db = (
        db.query(models_db.Client).filter(models_db.Client.user_id == client_id).first()
    )
    tags_db = (
        db.query(models_db.Tag).filter(models_db.Tag.id.in_(tags_id.tags_id)).all()
    )
    serializer = tags.ClientBase(user=client_db.users, tags=tags_db)
    for tag in tags_db:
        client_db.tags.append(tag)
    db.add(client_db)
    db.commit()
    return serializer


@router.delete("/client/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tags_from_client(
    id: int, tags_id: tags.TagsAdd, db: Session = Depends(get_db)
):
    """
    delete tags from client
    """
    client_db = (
        db.query(models_db.Client).filter(models_db.Client.user_id == id).first()
    )
    if not client_db:
        raise HTTPException(status_code=400, detail=f"No client with id: {id}.")
    tags_db = (
        db.query(models_db.Tag).filter(models_db.Tag.id.in_(tags_id.tags_id)).all()
    )
    for tag in tags_db:
        client_db.tags.remove(tag)
    db.commit()
    db.refresh(client_db)
    return client_db


@router.get("/client/{client_id}", response_model=tags.ClientBase, status_code=status.HTTP_200_OK)
def get_client_with_all_tags(client_id: int, db: Session = Depends(get_db)):
    """
    Get client by id with all tags
    """
    client_db = (
        db.query(models_db.Client).filter(models_db.Client.user_id == client_id).first()
    )
    if not client_db:
        raise HTTPException(status_code=400, detail=f"No client with id: {id}.")
    client_user = tags.User(
        id=client_db.users.id,
        username=client_db.users.username,
        email=client_db.users.email,
    )
    tags_db = (
        db.query(models_db.Tag).filter(models_db.Tag.clients.contains(client_db)).all()
    )
    # fields = db.query(models_db.Field).join(models_db.Tag).filter(models_db.Tag.clients.contains(client)).all()
    fields_db = (
        db.query(models_db.Field)
        .join(models_db.Tag)
        .filter(models_db.Tag.clients.contains(client_db))
        .all()
    )
    serializer = tags.ClientBase(user=client_user, tags=tags_db, fields=fields_db)
    return serializer
