from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.crud.post import create_post,get_post_by_id,get_post_by_user_id,get_post_score_by_user_id,update_post_by_id,del_post_by_id,get_all_post_url,get_post_url_by_id
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.post import PostBase, PostEdit, ShowPost

router = APIRouter(
    prefix="/post",
    tags=["Post"],
    responses={404: {"message": "Not found"}}
)


get_db = init_db.get_db


@router.post('/add_post', status_code=status.HTTP_201_CREATED)
async def add_post(request: PostBase, db: Session = Depends(get_db)):
    return create_post(request, db)

@router.get('/all')
async def get_all_post(db:Session = Depends(get_db)):
    return get_all_post_url(db)

@router.get('/{id}',response_model=ShowPost)
async def get_by_post_id(id,db:Session = Depends(get_db)):
    return get_post_by_id(id,db)

@router.get('/url/{id}')
async def get_url_by_post_id(id,db:Session = Depends(get_db)):
    return get_post_url_by_id(id,db)

@router.get('/user/{user_url}',response_model=List[ShowPost])
async def get_by_user_id(user_url,db:Session = Depends(get_db)):
    return get_post_by_user_id(user_url,db)

@router.get('/user/score/{user_url}')
async def get_score_by_user_id(user_url,db:Session = Depends(get_db)):
    return get_post_score_by_user_id(user_url,db)

@router.put('/update/{id}',status_code=status.HTTP_202_ACCEPTED)
async def update_post_by_ID(id,request:PostEdit,db:Session = Depends(get_db)):
    return update_post_by_id(id,request,db)

@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id,db:Session = Depends(get_db)):
    return del_post_by_id(id,db)