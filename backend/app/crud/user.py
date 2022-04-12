from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.schemas.user import UserBase,UserEditScore,UserEditProfile

def create_user(request:UserBase,db:Session):
    db_user = User(name = request.name,
                   profile_picture_url = request.profile_picture_url,
                   user_score = request.user_score)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(id,db:Session):
    user = db.query(User).filter(User.user_id == id).first()
    # ask
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
    return user

def get_score_by_ranking(db:Session):
    return db.query(User).order_by(User.user_score.desc()).all()

def get_score_by_name(db:Session):
    return db.query(User).order_by(User.name).all()

def update_user_score_by_id(id,request:UserEditScore,db:Session):
    user = db.query(User).filter(User.user_id == id)
    # ask
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
    # ask
    user.update(request.__dict__, synchronize_session="fetch")
    db.commit()
    return {'updated'}

def update_user_profile_by_id(id,request:UserEditProfile,db:Session):
    user = db.query(User).filter(User.user_id == id)
    # ask
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
    user.update(request.__dict__, synchronize_session="fetch")
    db.commit()
    return {'updated'}

# ask
def del_user_by_id(id,db:Session):
    user = db.query(User).filter(User.user_id == id)
    # ask
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an {id}")
    user.delete(synchronize_session=False)
    db.commit()
    # ask
    return {'done'}
