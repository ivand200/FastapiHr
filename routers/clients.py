from fastapi import APIRouter, Depends, HTTPException, Security, Header, status
from sqlalchemy.orm import Session

from models import models_db
from schemas import auth, clients
from db import get_db

router = APIRouter()


# We got Field, Tag, Client
# TODO: create/delete/get Field

@router.post("/fields/", response_model=clients.FieldBase, status_code=status.HTTP_201_CREATED)
async def create_field(field: clients.FieldCreate, db: Session = Depends(get_db)):
    """
    Create Field
    """
    check_field = db.query(models_db.Field).filter(models_db.Field.title == field.title).first()
    if check_field:
        raise HTTPException(status_code=400, detail="Field title already exists.")
    new_field = models_db.Field(title=field.title)
    db.add(new_field)
    db.commit()
    db.refresh(new_field)
    return new_field


@router.delete("/fields/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_field(id: int, db: Session = Depends(get_db)):
    """
    Delete Field by id
    """
    check_field = db.query(models_db.Field).filter(models_db.Field.id == id).first()
    if not check_field:
        raise HTTPException(status_code=400, detail="Can not find field id.")
    db.delete(check_field)
    db.commit()
    return f"field {check_field} was deleted"
