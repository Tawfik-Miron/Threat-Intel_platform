from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DB_PATH = os.getenv("SQLITE_PATH", "data/indicators.db")
DB_URL = f"sqlite:///{DB_PATH}"

# connect_args for sqlite to allow threads
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
