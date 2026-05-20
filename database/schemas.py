from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

class PostResponse(PostCreate):
    id: int

    class Config:
        orm_mode = True