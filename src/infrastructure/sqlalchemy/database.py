from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.infrastructure.settings.config import get_settings


class Base(DeclarativeBase):
    pass


def _url_sincronica() -> str:
    return get_settings().DATABASE_URL


engine: Engine = create_engine(
    _url_sincronica(),
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
