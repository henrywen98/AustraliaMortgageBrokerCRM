from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.api.deps import get_db, require_roles
from app.models import UserRole
from app.schemas.auth import LoginRequest, RegisterRequest, TokenPair
from app.services.auth import authenticate, issue_tokens, register_user
from app.core.security import decode_token, create_access_token
from app.core.config import settings
import redis


router = APIRouter()

_redis = None


def _get_redis():
    global _redis
    if _redis is None:
        try:
            _redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        except Exception:
            _redis = None
    return _redis


@router.post("/register", response_model=dict)
def register(payload: RegisterRequest, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.Admin))):
    u = register_user(db, payload.email, payload.password, payload.role)
    return {"id": u.id, "email": u.email, "role": u.role.value}


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = authenticate(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access, refresh = issue_tokens(user)
    r = _get_redis()
    if r:
        r.setex(f"refresh:{refresh}", settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600, user.id)
    response.set_cookie("refresh_token", refresh, httponly=True, samesite="lax")
    return TokenPair(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenPair)
def refresh_token(response: Response, refresh_token: str | None = None, db: Session = Depends(get_db)):
    token = refresh_token
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    data = decode_token(token)
    if not data or data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token")
    r = _get_redis()
    if r and not r.exists(f"refresh:{token}"):
        raise HTTPException(status_code=401, detail="Revoked token")
    user_id = data["sub"]
    # Lookup role fresh
    from app.models import User
    u = db.get(User, int(user_id))
    role = u.role.value if u else "Broker"
    access = create_access_token(user_id, role)
    return TokenPair(access_token=access, refresh_token=token)


@router.post("/logout", response_model=dict)
def logout(refresh_token: str):
    r = _get_redis()
    if r:
        r.delete(f"refresh:{refresh_token}")
    return {"ok": True}
