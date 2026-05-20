from fastapi import FastAPI, Depends
from database.database import Base, engine, get_db
from routers import posts, users
from database.model import User
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sql/")
def create_tables(db: Session = Depends(get_db)):
    return {
        'message' : "db table created successfully",
    }

