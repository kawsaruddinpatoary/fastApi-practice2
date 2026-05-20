from fastapi import APIRouter, Depends, HTTPException, status
from database.database import get_db, Base, engine
from database.model import User
from database.schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/")
def create_user(user : UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    new_user = db.query(User).filter(User.id == user_id).first()
    if new_user:
        return new_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.get("/search/", response_model=list[UserResponse])
def search_users(keyword: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.name.contains(keyword)).all()
    if len(users) > 0:
        return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found matching the keyword")

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user : UserCreate, db: Session = Depends(get_db)):
    new_user = db.query(User).filter(User.id == user_id).first()
    if new_user:
        new_user.name = user.name
        new_user.email = user.email
        db.commit()
        db.refresh(new_user)
        return new_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    new_user = db.query(User).filter(User.id == user_id).first()
    if new_user:
        db.delete(new_user)
        db.commit()
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")