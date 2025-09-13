from pydantic import BaseModel
from typing import Optional, List


class DealCreate(BaseModel):
    client_id: int
    lender: Optional[str] = None
    loan_type: Optional[str] = None
    amount: Optional[float] = None
    tags: List[str] = []
    due_date: Optional[str] = None  # ISO date


class DealRead(BaseModel):
    id: int
    client_id: int
    owner_user_id: Optional[int]
    lender: Optional[str]
    loan_type: Optional[str]
    amount: Optional[float]
    stage: str
    tags: List[str]
    due_date: Optional[str]

    class Config:
        from_attributes = True


class DealUpdate(BaseModel):
    lender: Optional[str] = None
    loan_type: Optional[str] = None
    amount: Optional[float] = None
    tags: Optional[List[str]] = None
    due_date: Optional[str] = None


class DealTransition(BaseModel):
    to_stage: str
