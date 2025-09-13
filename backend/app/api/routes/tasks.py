from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_db, get_current_user, broker_row_scope
from app.models import Task, Deal
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate


router = APIRouter()


@router.get("/", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db), owner_scope: int | None = Depends(broker_row_scope)):
    stmt = select(Task)
    if owner_scope is not None:
        # join via deal ownership
        deal_ids = [d.id for d in db.exec(select(Deal).where(Deal.owner_user_id == owner_scope)).all()]
        if deal_ids:
            stmt = stmt.where(Task.deal_id.in_(deal_ids))
        else:
            return []
    return db.exec(stmt).all()


@router.post("/", response_model=TaskRead)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    t = Task(**payload.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), owner_scope: int | None = Depends(broker_row_scope)):
    t = db.get(Task, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    if owner_scope is not None:
        d = db.get(Deal, t.deal_id)
        if not d or d.owner_user_id != owner_scope:
            raise HTTPException(status_code=403, detail="Forbidden")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(t, k, v)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.post("/assign", response_model=TaskRead)
def assign_task(task_id: int, assignee_user_id: int | None, db: Session = Depends(get_db), owner_scope: int | None = Depends(broker_row_scope)):
    t = db.get(Task, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    if owner_scope is not None:
        d = db.get(Deal, t.deal_id)
        if not d or d.owner_user_id != owner_scope:
            raise HTTPException(status_code=403, detail="Forbidden")
    t.assignee_user_id = assignee_user_id
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.post("/{task_id}/complete", response_model=TaskRead)
def complete_task(task_id: int, db: Session = Depends(get_db), owner_scope: int | None = Depends(broker_row_scope)):
    t = db.get(Task, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    if owner_scope is not None:
        d = db.get(Deal, t.deal_id)
        if not d or d.owner_user_id != owner_scope:
            raise HTTPException(status_code=403, detail="Forbidden")
    t.status = "done"
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db), owner_scope: int | None = Depends(broker_row_scope)):
    t = db.get(Task, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    if owner_scope is not None:
        d = db.get(Deal, t.deal_id)
        if not d or d.owner_user_id != owner_scope:
            raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(t)
    db.commit()
    return {"ok": True}

