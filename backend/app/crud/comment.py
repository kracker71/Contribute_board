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

    comment = Comment(comment_id=request.comment_id,
                    comment_content=request.comment_content,
                    comment_username=request.comment_username,
                    comment_profile_url=request.comment_profile_url,
                    comment_reaction_count=request.comment_reaction_count,
                    comment_score=request.comment_score,
                    comment_date_scraped=request.comment_date_scraped,
                    user_id=request.user_id,
                    post_id=request.post_id)
    db.add(comment)
    db.commit()
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

def update_comment_by_id(id:str,request:CommentEdit,db:Session):
    comment = db.query(Comment).filter(Comment.comment_id == id)
    
    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a comment with an id: {id}")
    
    comment.update({"comment_id":request.comment_id,
                    "comment_content":request.comment_content,
                    "comment_reaction_count":request.comment_reaction_count,
                    "comment_score":request.comment_score,
                    "comment_date_scraped":request.comment_date_scraped},synchronize_session="fetch")
    db.commit()
    return {'updated'}

def del_comment_by_id(id,db:Session):
    comment = db.query(Comment).filter(Comment.comment_id == id)
    
    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a comment with an id: {id}")
    
    comment.delete(synchronize_session=False)
    db.commit()
    return {'deleted'}
