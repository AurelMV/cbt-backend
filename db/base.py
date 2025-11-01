from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event
from sqlalchemy.engine import Engine

from core.config import Config

settings = Config()

DATABASE_URL = settings.DATABASE_URL

# Enable SQLite foreign key enforcement when using sqlite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    # Import models explicitly to ensure they're registered in SQLModel.metadata
    # before creating tables (important for tests/startup ordering)
    from db.models import (
        academic,
        location,
        programa,
        preinscripcion,
        enrollment,
    )  # noqa: F401

    SQLModel.metadata.create_all(engine)
