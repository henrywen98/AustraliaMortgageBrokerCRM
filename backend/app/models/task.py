from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deals.id")
    title: str
    assignee_user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    status: str = Field(default="open")
    priority: str = Field(default="normal")
    due_date: Optional[date] = None

