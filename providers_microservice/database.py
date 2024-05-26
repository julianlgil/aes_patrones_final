import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from databases import Database

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
providers_db = os.getenv('POSTGRES_DB')
DATABASE_URL = f"postgresql://{user}:{password}@localhost/{providers_db}"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
