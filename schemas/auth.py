from typing import List, Optional

from pydantic import BaseModel, validator, Field, EmailStr, ValidationError


class User(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr

    @validator("username")
    def valid_username(cls, value):
        if len(value) > 20:
            raise ValueError("Username should be up to 20 chars")
        return value

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str

    @validator("password")
    def valid_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password should be at least 8 chars")
        if not any(i.isdigit() for i in value):
            raise ValueError("Password should contains at least one number")
        if not any(i.isupper() for i in value):
            raise ValueError("Password should contains at least one capital letter")
        return value

    class Config:
        orm_mode = True
