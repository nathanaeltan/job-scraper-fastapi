from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv

load_dotenv()

postgres_user_name = os.getenv('POSTGRES_USERNAME')
postgres_password = os.getenv('POSTGRES_PASSWORD')

SQLALCHEMY_DATABASE_URL = f'postgresql://{postgres_user_name}:{postgres_password}@localhost/JobScraperDatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
