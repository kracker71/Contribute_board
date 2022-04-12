from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.post import Post
from backend.app.schemas.post import PostBase, PostEditScore, PostEditProfile

def create_post(request: PostBase, db:Session):
    pass

def get_post_by_id(id, db:Session):
    pass

def get_post_score_by_id(id, db:Session):
    pass

