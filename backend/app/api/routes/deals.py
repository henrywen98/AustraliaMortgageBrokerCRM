from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from app.api.deps import get_db, get_current_user, broker_row_scope
from app.models import Deal, DealStage
from app.schemas.deal import DealCreate, DealRead, DealUpdate, DealTransition
from app.services.audit import log_activity


router = APIRouter()


@router.get("/", response_model=list[DealRead])
def list_deals(
    db: Session = Depends(get_db),
    owner_scope: int | None = Depends(broker_row_scope),
):
    stmt = select(Deal)
    if owner_scope is not None:
        stmt = stmt.where(Deal.owner_user_id == owner_scope)
    return db.exec(stmt).all()


@router.post("/", response_model=DealRead)
def create_deal(payload: DealCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    d = Deal(**payload.model_dump(), owner_user_id=user.id)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


@router.put("/{deal_id}", response_model=DealRead)
def update_deal(
    deal_id: int,
    payload: DealUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    owner_scope: int | None = Depends(broker_row_scope),
    request: Request | None = None,
):
    d = db.get(Deal, deal_id)
    if not d:
        raise HTTPException(status_code=404, detail="Not found")
    if owner_scope is not None and d.owner_user_id != owner_scope:
        raise HTTPException(status_code=403, detail="Forbidden")
    old = d.model_dump()
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(d, k, v)
    db.add(d)
    db.commit()
    db.refresh(d)
    log_activity(
        db,
        actor_user_id=user.id,
        entity_type="deal",
        entity_id=d.id,
        action="update",
        diff={"before": old, "after": d.model_dump()},
        ip=request.client.host if request and request.client else None,
    )
    return d


@router.post("/{deal_id}/transition", response_model=DealRead)
def transition_deal(
    deal_id: int,
    payload: DealTransition,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    owner_scope: int | None = Depends(broker_row_scope),
    request: Request | None = None,
):
    d = db.get(Deal, deal_id)
    if not d:
        raise HTTPException(status_code=404, detail="Not found")
    if owner_scope is not None and d.owner_user_id != owner_scope:
        raise HTTPException(status_code=403, detail="Forbidden")
    allowed = [e.value for e in DealStage]
    if payload.to_stage not in allowed:
        raise HTTPException(status_code=400, detail="Invalid stage")
    old_stage = d.stage.value
    d.stage = DealStage(payload.to_stage)
    db.add(d)
    db.commit()
    db.refresh(d)
    log_activity(
        db,
        actor_user_id=user.id,
        entity_type="deal",
        entity_id=d.id,
        action="transition",
        diff={"stage": {"from": old_stage, "to": d.stage.value}},
        ip=request.client.host if request and request.client else None,
    )
    return d


@router.delete("/{deal_id}", response_model=dict)
def delete_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    owner_scope: int | None = Depends(broker_row_scope),
):
    d = db.get(Deal, deal_id)
    if not d:
        raise HTTPException(status_code=404, detail="Not found")
    if owner_scope is not None and d.owner_user_id != owner_scope:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(d)
    db.commit()
    return {"ok": True}

