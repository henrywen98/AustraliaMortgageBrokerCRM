from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    Broker = "Broker"
    Processor = "Processor"
    Admin = "Admin"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.Broker)
    active: bool = Field(default=True)

