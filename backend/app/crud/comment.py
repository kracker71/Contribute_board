from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.models.user import User
from app.models.post import Post
from app.crud.post import get_post_id_by_url
from app.crud.user import get_user_by_id
from app.schemas.comment import CommentCreate,CommentEdit

 
def create_comment(request:CommentCreate,db:Session):
    
    tmp_comment = db.query(Comment).filter(Comment.comment_id == request.comment_id).first()
    if tmp_comment:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Already exists")
    
    db_comment = Comment(comment_id = request.comment_id,
                         comment_data = request.comment_content,
                         date_comment = request.comment_date,
                         comment_likes = request.comment_like,
                         comment_score = request.comment_score,
                         user_url = request.user_url,
                         post_url = request.post_url)
    
    db.add(db_comment)
    db.commit()
    user = get_user_by_id(request.user_url,db)
    post = get_post_id_by_url(request.post_url,db)
    db_comment.user_id = user.user_id
    db_comment.post_id = post.post_id
    db.commit()
    db.refresh(db_comment)
    return db_comment

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



def update_comment_by_id(commentID,request:CommentEdit,db:Session):
    comment = db.query(Comment).filter(Comment.comment_id == commentID)
    
    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a comment with an id: {id}")
    
    comment.update(request.__dict__,synchronize_session="fetch")
    db.commit()
    return {'updated'}

def del_comment_by_id(commentID,db:Session):
    comment = db.query(Comment).filter(Comment.comment_id == commentID)
    
    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a comment with an id: {id}")
    
    comment.delete(synchronize_session=False)
    db.commit()
    return {'deleted'}
