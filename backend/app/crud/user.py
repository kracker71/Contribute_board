from fastapi import HTTPException, status
from sqlalchemy.orm import Session ,load_only
from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User
from app.schemas.user import UserRegister,UserEditScore,UserEditProfile

def create_user(request:UserRegister,db:Session):
    # check if user already exist
    is_user_existed = db.query(User).filter(
        User.user_id == request.user_id
        ).first()
    if is_user_existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user with an {request.user_id} already existed")
    user = User(**request.__dict__)
    db.add(user)
    db.commit()
    return {'created'}

def get_all_user(db:Session):
    return db.query(User).all()

def get_user_by_id(id:str,db:Session):
    user = db.query(User).filter(User.user_id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
    return user

def get_score_order_by_ranking(db:Session):
    return db.query(User).order_by(User.user_score.desc()).all()

def get_score_order_by_name(db:Session):
    return db.query(User).order_by(User.user_name).all()

#####post section######
def get_posts_by_user_id(user_id, db:Session):
    post = db.query(Post).filter(Post.user_id == user_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a post with an id {id}")
    return post.all()

def get_user_posts_score(id,db:Session):
    user_posts = get_posts_by_user_id(id,db)
    score = 0.0
    for post in user_posts:
        score += post.post_score
    return score

#####comment section######
def get_comments_by_user_id(id,db:Session):
    user = db.query(User).filter(User.user_id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a user with an id: {id}")
    return db.query(Comment).filter(Comment.user_id == id).all()

def get_user_comments_score(id,db:Session):
    user_comments = get_comments_by_user_id(id,db)
    score = 0.0
    for comment in user_comments:
        score+= comment.comment_score
    return score

def update_user_score_by_id(id,request:UserEditScore,db:Session):
    user = db.query(User).filter(User.profile_url == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
        
    new_score = get_user_posts_score(id,db)
    new_score += get_user_comments_score(id,db)
    
    user.update({"user_score":new_score,
                 "user_update_score_date":request.user_update_score_date}, 
                 synchronize_session="fetch")
    db.commit()
    return {'updated'}

def update_user_profile_by_id(id,request:UserEditProfile,db:Session):
    user = db.query(User).filter(User.user_id == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
        
    user.update(request.__dict__, synchronize_session="fetch")
    db.commit()
    return {'updated'}

def update_all_user_score (request : UserEditScore,db:Session):
    users = db.query(User).options(load_only("user_id")).all()
    for user in users:
        update_user_score_by_id(user.user_id,request,db)
    return {'updated'}

def del_user_by_id(id,db:Session):
    user = db.query(User).filter(User.user_id == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
    user.delete(synchronize_session=False)
    db.commit()
    
    return {'done'}
