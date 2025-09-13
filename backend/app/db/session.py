from sqlalchemy import create_engine
from sqlmodel import Session
from app.core.config import settings


engine = create_engine(settings.DB_URL, pool_pre_ping=True, future=True)


def get_session():
    with Session(engine) as session:
        yield session

