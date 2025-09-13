from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    id: int
    email: EmailStr
    role: str
    active: bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "Broker"


class UserUpdate(BaseModel):
    role: Optional[str] = None
    active: Optional[bool] = None

