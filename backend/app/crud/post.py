from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostBase, PostEditScore, PostEditData
from app.database import init_db

def create_post(request: PostBase, db:Session):
    print("yay")
    db_post = Post(post_id=request.post_id,
                   post_data=request.post_data,
                   post_url=request.post_url,
                   date_scrape=request.date_scrape,
                   date_post=request.date_post,
                   post_score=request.post_score,
                   post_likes=request.post_likes)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


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


# def test():    
#     get_db = init_db.get_db
#     create_post(PostBase, get_db)
#     print('pass')


# if __name__ == '__main__':
#     test()