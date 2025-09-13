from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_db, get_current_user, require_roles
from app.models import User, UserRole
from app.schemas.user import UserBase, UserCreate, UserUpdate
from app.core.security import hash_password


router = APIRouter()


@router.get("/me", response_model=UserBase)
def me(user=Depends(get_current_user)):
    return user


@router.get("/", response_model=list[UserBase])
def list_users(db: Session = Depends(get_db), user=Depends(require_roles(UserRole.Admin))):
    return db.exec(select(User)).all()


@router.post("/", response_model=UserBase)
def create_user(payload: UserCreate, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.Admin))):
    u = User(email=payload.email, hashed_password=hash_password(payload.password), role=UserRole(payload.role))
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.put("/{user_id}", response_model=UserBase)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.Admin))):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="Not found")
    if payload.role is not None:
        u.role = UserRole(payload.role)
    if payload.active is not None:
        u.active = payload.active
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.Admin))):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(u)
    db.commit()
    return {"ok": True}

