from fastapi import FastAPI, Depends
from database.database import Base, engine, get_db
from database.model import User
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sql/")
def read_users(db: Session = Depends(get_db)):
    return {
        'message' : "db table created successfully",
    }

@app.post("/user/")
def create_user(user_name: str, db: Session = Depends(get_db)):
    new_user = User(name=user_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    new_user = db.query(User).filter(User.id == user_id).first()
    if new_user:
        return new_user
    return {"message": "User not found"}

@app.put("/users/{user_id}")
def update_user(user_id: int, user_name: str, db: Session = Depends(get_db)):
    new_user = db.query(User).filter(User.id == user_id).first()
    if new_user:
        new_user.name = user_name
        db.commit()
        db.refresh(new_user)
        return new_user
    return {"message": "User not found"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    new_user = db.query(User).filter(User.id == user_id).first()
    if new_user:
        db.delete(new_user)
        db.commit()
        return {"message": "User deleted successfully"}
    return {"message": "User not found"}