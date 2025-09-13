from typing import Optional
from sqlmodel import Session, select
from app.models import User, UserRole
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token


def register_user(db: Session, email: str, password: str, role: str = "Broker") -> User:
    existing = db.exec(select(User).where(User.email == email)).first()
    if existing:
        raise ValueError("Email already registered")
    user = User(email=email, hashed_password=hash_password(password), role=UserRole(role))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = db.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def issue_tokens(user: User) -> tuple[str, str]:
    return create_access_token(str(user.id), user.role.value), create_refresh_token(str(user.id))

