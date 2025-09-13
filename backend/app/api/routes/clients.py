from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_db, get_current_user, require_roles
from app.models import Client, UserRole
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate


router = APIRouter()


@router.get("/", response_model=list[ClientRead])
def list_clients(db: Session = Depends(get_db), user=Depends(get_current_user)):
    # MVP: All roles can list clients; refine later for strict linkage
    return db.exec(select(Client)).all()


@router.post("/", response_model=ClientRead)
def create_client(payload: ClientCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = Client(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.put("/{client_id}", response_model=ClientRead)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.get(Client, client_id)
    if not c:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.delete("/{client_id}", response_model=dict)
def delete_client(client_id: int, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.Admin))):
    c = db.get(Client, client_id)
    if not c:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(c)
    db.commit()
    return {"ok": True}

