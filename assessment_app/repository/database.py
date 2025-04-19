# assessment_app/repository/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/user"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from assessment_app.models import *  # This will register all tables properly


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
