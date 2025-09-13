from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON


class Client(SQLModel, table=True):
    __tablename__ = "clients"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    contact: Dict[str, Any] = Field(sa_column=Column(JSON))
    notes: Optional[str] = None
    pii_masked_fields: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
