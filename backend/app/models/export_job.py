from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class ExportJob(SQLModel, table=True):
    __tablename__ = "export_jobs"

    id: Optional[int] = Field(default=None, primary_key=True)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None
    status: str = Field(default="pending")  # pending|running|success|failed
    file_uri: Optional[str] = None
    rows_count: int = Field(default=0)
    checksum: Optional[str] = None

