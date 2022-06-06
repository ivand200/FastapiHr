from fastapi import (
    APIRouter,
    Depends, HTTPException,
    Security,
    Header,
    status,
    Body,
    Form,
    Request,
    Query
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

@router.get("/test")
def add_tags_to_client(name: str = Body(...), age: int = Body(...)):
    return {"name": name, "age": age}


@router.post("/{client_id}", response_model=auth.User)
def add_tags_to_client(client_id: int, tags_id: tags.TagsAdd, db: Session = Depends(get_db)):
    """
    Add tags to client
    """
    client = db.query(models_db.Client).filter(models_db.Client.user_id == client_id).first()
    tags = db.query(models_db.Tag).filter(models_db.Tag.id.in_(tags_id.tags_id)).all()
    print(tags_id.tags_id)
    for tag in tags:
        client.tags.append(tag)
        print(client.tags)
    db.add(client)
    db.commit()
    return client.users


@router.get("/{client_id}")
def get_client_with_all_tags(client_id: int, db: Session = Depends(get_db)):
    """
    TODO: ...
    """
    client = db.query(models_db.Client).filter(models_db.Client.user_id == client_id).first()
    # print(client.tags)
    client_user = tags.User(id=client.users.id, username=client.users.username, email=client.users.email)
    tags = db.query(models_db.Tag).filter(models_db.Tag.clients.contains(client)).all()
    # fields = db.query(models_db.Field).join(models_db.Tag).filter(models_db.Tag.clients.contains(client)).all()
    fields = db.query(models_db.Field).join(models_db.Tag).filter(models_db.Tag.clients.contains(client)).all()
    print(fields)
    serializer = tags.ClientBase(user=client_user, tags=tags, fields=fields)
    return serializer
