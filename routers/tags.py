from fastapi import APIRouter, Depends, HTTPException, Security, Header, status
from sqlalchemy.orm import Session

from typing import List

from models import models_db
from schemas import auth, tags
from db import get_db

router = APIRouter()


@router.get("/fields", response_model=List[tags.FieldBase], status_code=status.HTTP_200_OK)
async def get_all_fields(db: Session = Depends(get_db)):
    """
    Get all fields
    """
    fields = db.query(models_db.Field).all()
    return fields


@router.post("/fields", response_model=tags.FieldBase, status_code=status.HTTP_201_CREATED)
async def create_field(field: tags.FieldCreate, db: Session = Depends(get_db)):
    """
    Create Field
    """
    field_db = (
        db.query(models_db.Field).filter(models_db.Field.title == field.title).first()
    )
    if field_db:
        raise HTTPException(status_code=400, detail="Field title already exists.")
    new_field = models_db.Field(title=field.title)
    db.add(new_field)
    db.commit()
    db.refresh(new_field)
    return new_field


@router.delete("/fields/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.get("/fields/{id}", response_model=tags.FieldTags, status_code=status.HTTP_200_OK)
async def get_field_by_id(id: int, db: Session = Depends(get_db)):
    """
    Get field by id with all tags
    """
    # field = db.query(models_db.Field, models_db.Tag).join(models_db.Tag).filter(models_db.Field.id == id).all()
    field_db = db.query(models_db.Field).filter(models_db.Field.id == id).first()
    if not field_db:
        raise HTTPException(status_code=400, detail="Can not find field id.")
    tags_db = db.query(models_db.Tag).filter(models_db.Tag.field_id == id).all()
    result = tags.FieldTags(field=field_db, tags=tags_db)
    return result


@router.put("/fields/{id}",  response_model=tags.FieldBase, status_code=status.HTTP_200_OK)
async def update_field(
    id: int, field: tags.FieldCreate, db: Session = Depends(get_db)
):
    """
    Update existing field
    """
    field_db = db.query(models_db.Field).filter(models_db.Field.id == id).first()
    if not field_db:
        raise HTTPException(status_code=400, detail="Can not find field id.")
    field_db.title = field.title
    db.commit()
    db.refresh(field_db)
    return field_db


@router.get("/tag", response_model=List[tags.TagPublic], status_code=status.HTTP_200_OK)
async def get_all_tags(db: Session = Depends(get_db)):
    """
    Get all tags
    """
    tags_db = db.query(models_db.Tag).all()
    return tags_db


@router.post("/tag", response_model=tags.TagPublic, status_code=status.HTTP_201_CREATED)
async def create_tags(tag: tags.TagCreate, db: Session = Depends(get_db)):
    """
    Create a tag
    with field id
    """
    new_tag = db.query(models_db.Tag).filter(models_db.Tag.title == tag.title).first()
    if new_tag:
        raise HTTPException(
            status_code=400, detail="Tag with this title already exists."
        )
    new_tag = models_db.Tag(title=tag.title, field_id=tag.field_id)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@router.delete("/tag/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tags(id: int, db: Session = Depends(get_db)):
    """
    Delete tag by id
    """
    tag_db = db.query(models_db.Tag).filter(models_db.Tag.id == id).first()
    if not tag_db:
        raise HTTPException(status_code=400, detail=f"No tag with id: {id}.")
    db.delete(tag_db)
    db.commit()
    return tag_db
