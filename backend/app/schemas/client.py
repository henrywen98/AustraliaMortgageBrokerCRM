from pydantic import BaseModel
from typing import Optional, Dict, Any


class ClientCreate(BaseModel):
    name: str
    contact: Dict[str, Any] = {}
    notes: Optional[str] = None


class ClientRead(BaseModel):
    id: int
    name: str
    contact: Dict[str, Any]
    notes: Optional[str]

    class Config:
        from_attributes = True


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

