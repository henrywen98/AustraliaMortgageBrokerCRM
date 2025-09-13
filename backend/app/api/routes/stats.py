from fastapi import APIRouter, Depends
from datetime import datetime
from sqlmodel import Session, select
from app.api.deps import get_db, broker_row_scope
from app.models import Deal
from typing import Optional


router = APIRouter()


@router.get("/summary", response_model=dict)
def summary(
    db: Session = Depends(get_db),
    owner_scope: Optional[int] = Depends(broker_row_scope),
    start: Optional[str] = None,
    end: Optional[str] = None,
):
    stmt = select(Deal)
    if owner_scope is not None:
        stmt = stmt.where(Deal.owner_user_id == owner_scope)
    deals = db.exec(stmt).all()
    def count_stage(stage: str):
        return sum(1 for d in deals if d.stage.value == stage)
    total_amount_settlement = sum((d.amount or 0) for d in deals if d.stage.value == "Settlement")
    return {
        "enquiry": count_stage("Enquiry"),
        "submission": count_stage("Submission"),
        "approval": count_stage("Approval"),
        "settlement_amount": total_amount_settlement,
    }


@router.get("/funnel", response_model=dict)
def funnel(
    db: Session = Depends(get_db),
    owner_scope: Optional[int] = Depends(broker_row_scope),
):
    stmt = select(Deal)
    if owner_scope is not None:
        stmt = stmt.where(Deal.owner_user_id == owner_scope)
    deals = db.exec(stmt).all()
    stages = ["Enquiry","Checklist Sent","Submission","Approval","Settlement"]
    return {s: sum(1 for d in deals if d.stage.value == s) for s in stages}
