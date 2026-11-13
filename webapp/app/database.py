import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

DB_PATH = BASE_DIR / "estudantes.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{DB_PATH}"

if SQLALCHEMY_DATABASE_URL.startswith(("postgres://", "postgresql://")):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgres://", "postgresql+psycopg://", 1
    ).replace("postgresql://", "postgresql+psycopg://", 1)

engine_options = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
