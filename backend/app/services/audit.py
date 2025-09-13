from typing import Any, Dict
from sqlmodel import Session
from app.models import ActivityLog


def log_activity(
    db: Session,
    actor_user_id: int | None,
    entity_type: str,
    entity_id: int,
    action: str,
    diff: Dict[str, Any] | None = None,
    ip: str | None = None,
):
    log = ActivityLog(
        actor_user_id=actor_user_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        diff_json=diff or {},
        ip=ip,
    )
    db.add(log)
    db.commit()

