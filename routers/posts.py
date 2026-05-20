from fastapi import APIRouter, Depends, HTTPException, status
from database.database import get_db, Base, engine
from database.model import Post, User 
from database.schemas import PostCreate, PostResponse
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("/")
def create_post(post : PostCreate, db: Session = Depends(get_db)):
    new_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    new_post = db.query(Post).filter(Post.id == post_id).first()
    if new_post:
        return new_post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@router.get("/user/{user_id}", response_model=list[PostResponse])
def get_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    if len(posts) > 0:
        return posts
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found for this user")

@router.get("/search/", response_model=list[PostResponse])
def search_posts(keyword: str, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.title.contains(keyword) | Post.content.contains(keyword)).all()
    if len(posts) > 0:
        return posts
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found matching the keyword")

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post : PostCreate, db: Session = Depends(get_db)):
    new_post = db.query(Post).filter(Post.id == post_id).first()
    if new_post:
        new_post.title = post.title
        new_post.content = post.content
        new_post.user_id = post.user_id
        db.commit()
        db.refresh(new_post)
        return new_post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    new_post = db.query(Post).filter(Post.id == post_id).first()
    if new_post:
        db.delete(new_post)
        db.commit()
        return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")