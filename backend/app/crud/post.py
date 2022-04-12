from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.post import Post
from backend.app.schemas.post import PostBase, PostEditScore, PostEditData

def create_post(request: PostBase, db:Session):
    pass

def get_post_by_id(id, db:Session):
    pass

def get_post_score_by_id(id, db:Session):
    pass

def update_post_score_by_id(id, request:PostEditScore, db:Session):
    pass

def update_post_data_by_id(id, request:PostEditData, db:Session):
    pass


def del_post_by_id(id, db:Session):
    pass
