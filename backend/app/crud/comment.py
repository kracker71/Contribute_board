from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.models.user import User
from app.models.post import Post
from app.crud.post import get_post_id_by_url
from app.crud.user import get_user_by_id
from app.schemas.comment import CommentCreate,CommentEdit

def create_comment(request:CommentCreate,db:Session):
    is_comment_existed = db.query(Comment).filter(Comment.comment_id == request.comment_id).first()
    if is_comment_existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail=f"comment with an id {request.comment_id} already existed")

    comment = Comment(**request.__dict__)
    db.add(comment)
    post_id = get_post_id_by_url(request.post_id,db)
    user_id = get_user_by_id(request.user_id,db)
    comment.post_id = post_id
    comment.user_id = user_id
    db.commit()
    db.refresh(comment)
    return {'created'}

def get_comment_by_id(id,db:Session):
    comment = db.query(Comment).filter(Comment.comment_id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a comment with an id: {id}")
    return comment

def get_all_comment_by_post_id(id,db:Session):
    post = db.query(Post).filter(Post.post_id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a post with an id: {id}")
    return db.query(Comment).filter(Comment.post_id == id).all()

def get_comment_score_by_id(id,db:Session):
    comment = db.query(Comment).filter(Comment.comment_id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a comment with an id: {id}")
    return comment.comment_score

def update_comment_by_id(id,request:CommentEdit,db:Session):
    comment = db.query(Comment).filter(Comment.comment_id == id)
    
    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a comment with an id: {id}")
    
    comment.update(request.__dict__,synchronize_session="fetch")
    db.commit()
    return {'updated'}

def del_comment_by_id(id,db:Session):
    comment = db.query(Comment).filter(Comment.comment_id == id)
    
    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a comment with an id: {id}")
    
    comment.delete(synchronize_session=False)
    db.commit()
    return {'deleted'}
