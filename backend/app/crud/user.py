from fastapi import HTTPException, status
from sqlalchemy.orm import Session ,load_only
from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User
from app.schemas.user import UserRegister,UserEditScore,UserEditProfile


def create_user(request:UserRegister,db:Session):
    
    tmp_user = db.query(User).filter(User.profile_url == request.profile_url).first()
    if tmp_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="already exists")
    
    db_user = User(name = request.name,
                   profile_picture_url = request.profile_picture_url,
                   profile_url = request.profile_url,
                   user_score = request.user_score,
                   update_score_date = request.update_score_date)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_user(db:Session):
    return db.query(User).all()

def get_user_by_id(id:str,db:Session):
    user = db.query(User).filter(User.profile_url == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
    return user

def get_score_by_ranking(db:Session):
    return db.query(User).order_by(User.user_score.desc()).all()

def get_score_by_name(db:Session):
    return db.query(User).order_by(User.name).all()

#####post section######
def get_post_by_user_id(user_url, db:Session):
    post = db.query(Post).filter(Post.user_url == user_url)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a post with an id {id}")
    return post.all()

def get_post_score_by_user_id(user_url, db:Session):
    post = get_post_by_user_id(user_url,db)
    score = 0.0
    for x in post:
        score += x.post_score 
    return score

#####comment section######
def get_all_comment_by_user_id(id,db:Session):
    user = db.query(User).filter(User.profile_url == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found a user with an id: {id}")
    return db.query(Comment).filter(Comment.user_url == id).all()

def get_total_score_by_user_id(id,db:Session):
    comment = get_all_comment_by_user_id(id,db)
    score = 0.0
    for x in comment:
        score+= x.comment_score
    return score

def update_user_score_by_id(id,request:UserEditScore,db:Session):
    user = db.query(User).filter(User.profile_url == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
        
    new_score = 0
    new_score += get_post_score_by_user_id(id,db)
    new_score += get_total_score_by_user_id(id,db)
    
    user.update({"user_score":new_score,
                 "update_score_date":request.update_score_date}, synchronize_session="fetch")
    db.commit()
    return {'updated'}


def update_user_profile_by_id(id,request:UserEditProfile,db:Session):
    user = db.query(User).filter(User.profile_url == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
        
    user.update(request.__dict__, synchronize_session="fetch")
    db.commit()
    return {'updated'}

def update_all_user_score (request : UserEditScore,db:Session):
    users = db.query(User).options(load_only("profile_url")).all()
    for user in users:
        update_user_score_by_id(user.profile_url,request,db)
    return {'updated'}


def del_user_by_id(id,db:Session):
    user = db.query(User).filter(User.profile_url == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
    user.delete(synchronize_session=False)
    db.commit()
    
    return {'done'}
