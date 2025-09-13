from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from app.db.session import get_session
from app.core.security import decode_token
from app.models import User, UserRole
from typing import Optional


bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Session:
    yield from get_session()


def get_current_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if not creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    data = decode_token(creds.credentials)
    if not data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.exec(select(User).where(User.id == int(data["sub"])) ).first()
    if not user or not user.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User inactive")
    return user


def require_roles(*roles: UserRole):
    def _dep(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user
    return _dep


def broker_row_scope(user: User = Depends(get_current_user)) -> Optional[int]:
    # Brokers only see their own; Admin/Processor get None (no extra filter)
    if user.role == UserRole.Broker:
        return user.id
    return None
