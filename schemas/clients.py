from typing import List, Optional

from pydantic import BaseModel, validator, Field


class FieldCreate(BaseModel):
    title: str

    class Config:
        orm_mode = True


class FieldBase(FieldCreate):
    id: int

    class Config:
        orm_mode = True
