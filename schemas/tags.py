from typing import List, Optional

from pydantic import BaseModel, validator, Field

from .auth import User


class FieldCreate(BaseModel):
    title: str

    class Config:
        orm_mode = True


class FieldBase(FieldCreate):
    id: int

    class Config:
        orm_mode = True


class TagCreate(BaseModel):
    title: str
    field_id: int

    class Config:
        orm_mode = True


class TagPublic(TagCreate):
    id: Optional[int]

    class Config:
        orm_mode = True


class TagsAdd(BaseModel):
    tags_id: List[int]

    class Config:
        orm_mode = True


class FieldTags(BaseModel):
    field: Optional[FieldBase]
    tags: Optional[List[TagPublic]]

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    user: Optional[User]
    fields: Optional[List[FieldBase]]
    tags: Optional[List[TagPublic]]

    class Config:
        orm_mode = True
