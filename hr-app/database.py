import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL=os.getenv('SQLALCHEMY_DATABASE_URL')
SQLALCHEMY_DATABASE_URL="postgresql://root:root@pgdatabase:5432/globantds"
engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    client_encoding='utf-8'
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
