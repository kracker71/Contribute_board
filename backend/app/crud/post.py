from fastapi import HTTPException, status
from sqlalchemy.orm import Session,load_only
from app.models.post import Post
from app.models.user import User
from app.crud.user import get_user_by_id
from app.schemas.post import PostBase, PostEdit,PostCreate
from app.database import init_db

def create_post(request:PostBase, db:Session):
    # Check if post already exist
    is_post_existed = db.query(Post).filter(Post.post_id == request.post_id).first()
    if is_post_existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"post with an id {request.post_id} already existed")

    post = Post(**request.__dict__)
    db.add(post)
    db.commit()
    user = get_user_by_id(request.user_id, db)
    post.user_id = user.user_id
    db.commit()
    db.refresh(post)
    return {'created'}

def get_post(db:Session,limit = None,offset=0):
    return db.query(Post).offset(offset).limit(limit).all()

def get_all_post_id(db:Session):
    return db.query(Post).options(load_only("post_id")).all()

def get_all_post_url(db:Session):
    return db.query(Post).options(load_only("post_url")).all()

def get_post_url_by_id(id, db:Session):
    post = db.query(Post).filter(Post.post_id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a post with an id {id}")
    return post.options(load_only("post_url")).one()

def get_post_id_by_url(url, db:Session):
    post = db.query(Post).filter(Post.post_url == url)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a post with a url {url}")
    return post.options(load_only("post_id")).one()

def get_post_by_id(id, db:Session):
    post = db.query(Post).filter(Post.post_id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a post with an id {id}")
    return post

def get_post_score_by_id(id, db:Session):
    post = db.query(Post).filter(Post.post_id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a post with an id {id}")
    return post.options(load_only("post_score")).one()

def update_post_by_id(id, request:PostEdit, db:Session):
    post = db.query(Post).filter(Post.post_id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a post with an id {id}")
    post.update(request.__dict__,synchronize_session="fetch")
    db.commit()
    return {'updated'}

def init_post_data_by_id(id:str, request:PostCreate, db:Session):
    post = db.query(Post).filter(Post.post_id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a post with an id {id}")
    post.update(request,synchronize_session="fetch")
    db.commit()
    return {'updated'}

def del_post_by_id(id, db:Session):
    post = db.query(Post).filter(Post.post_id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a post with an id {id}")
    post.update(synchronize_session=False)
    db.commit()
    return {'deleted'}