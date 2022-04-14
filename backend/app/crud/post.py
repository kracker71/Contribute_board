from fastapi import HTTPException, status
from sqlalchemy.orm import Session,load_only
from app.models.post import Post
from app.models.user import User
from app.crud.user import get_user_by_id
from app.schemas.post import PostBase, PostEdit
from app.database import init_db

def create_post(request: PostBase, db:Session):
    
    tmp_post = db.query(Post).filter(Post.post_id == request.post_id).first()
    if tmp_post:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="already exists")

    db_post = Post(post_id=request.post_id,
                   post_data=request.post_data,
                   post_url=request.post_url,
                   date_scrape=request.date_scrape,
                   date_post=request.date_post,
                   post_score=request.post_score,
                   post_likes=request.post_likes,
                   user_url=request.user_url)
    
    db.add(db_post)
    db.commit()
    user = get_user_by_id(request.user_url,db)
    print(user)
    db_post.user_id = user.user_id
    db.commit()
    db.refresh(db_post)
    return db_post

def get_all_post_url(db:Session):
    return db.query(Post).options(load_only("post_url")).all()

def get_post_url_by_id(id, db:Session):
    post = db.query(Post).filter(Post.post_id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an id {id}")
    return post.options(load_only("post_url")).one()

def get_post_by_id(id, db:Session):
    post = db.query(Post).filter(Post.post_id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an id {id}")
    return post

def get_post_by_user_id(user_url, db:Session):
    post = db.query(Post).filter(Post.user_url == user_url)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an id {id}")
    return post.all()

def get_post_score_by_user_id(user_url, db:Session):
    post = get_post_by_user_id(user_url,db)
    score = 0.0
    for x in post:
        score += x.post_score 
    return score

def update_post_by_id(id, request:PostEdit, db:Session):
    post = db.query(Post).filter(Post.post_id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an id {id}")
    post.update(request.__dict__,synchronize_session="fetch")
    db.commit()
    return {'updated'}


def del_post_by_id(id, db:Session):
    post = db.query(Post).filter(Post.post_id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found a user with an id {id}")
    post.update(synchronize_session=False)
    db.commit()
    return {'deleted'}


# def test():    
#     get_db = init_db.get_db
#     create_post(PostBase, get_db)
#     print('pass')


# if __name__ == '__main__':
#     test()