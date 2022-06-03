from typing import List, Optional

from pydantic import BaseModel, validator, Field


class User(BaseModel):
    id: Optional[int]
    username: str
    email: str

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str

    class Config:
        orm_mode = True
