from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, JSON


class ActivityLog(SQLModel, table=True):
    __tablename__ = "activity_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    actor_user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    entity_type: str
    entity_id: int
    action: str
    diff_json: Dict[str, Any] = Field(default_factory=dict, sa_column_kwargs={"type_": JSON})
    ip: Optional[str] = None
    ts: datetime = Field(default_factory=datetime.utcnow)

