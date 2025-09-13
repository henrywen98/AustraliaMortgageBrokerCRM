from .session import engine
from sqlmodel import SQLModel


def init_db():
    SQLModel.metadata.create_all(engine)

