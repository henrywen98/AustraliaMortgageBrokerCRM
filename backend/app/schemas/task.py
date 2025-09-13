from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    deal_id: int
    title: str
    assignee_user_id: Optional[int] = None
    due_date: Optional[str] = None
    priority: Optional[str] = "normal"


class TaskRead(BaseModel):
    id: int
    deal_id: int
    title: str
    assignee_user_id: int | None
    status: str
    priority: str
    due_date: str | None

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    assignee_user_id: Optional[int] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

