from typing import Optional, List
from enum import Enum
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Column, ARRAY


class DealStage(str, Enum):
    Enquiry = "Enquiry"
    ChecklistSent = "Checklist Sent"
    Submission = "Submission"
    Approval = "Approval"
    Settlement = "Settlement"


class Deal(SQLModel, table=True):
    __tablename__ = "deals"

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.id")
    owner_user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    lender: Optional[str] = None
    loan_type: Optional[str] = None
    amount: Optional[float] = None
    stage: DealStage = Field(default=DealStage.Enquiry)
    tags: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(item_type=str)))
    due_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

