from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# create database url
user = 'root'
password = 'root'
host = 'localhost'
port = '3306'
database = 'fastapi_pro1'
DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

#create engine
engine = create_engine(DATABASE_URL)

# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for models
Base = declarative_base()

#provide session to the application
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()