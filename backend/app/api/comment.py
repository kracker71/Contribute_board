from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.crud.comment import (
    create_comment, 
    get_comment_by_id, 
    get_all_comment_by_post_id, 
    update_comment_by_id, 
    del_comment_by_id, 
    get_comment_score_by_id,
)
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate,CommentEdit,ShowComment

router = APIRouter(
    prefix="/comment",
    tags=["Comment"],
    responses={404: {"message": "Not found"}}
)

get_db = init_db.get_db

@router.post('/add_comment', status_code=status.HTTP_201_CREATED)
async def add_comment(request: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(request, db)

@router.get('/{id}',response_model=ShowComment)
async def get_by_comment_id(id,db:Session = Depends(get_db)):
    return get_comment_by_id(id,db)

@router.get('/{id}/score',response_model=float)
async def get_score_by_id(id,db:Session = Depends(get_db)):
    return get_comment_score_by_id(id,db)

@router.get('/post/{post_id}',response_model=List[ShowComment])
async def get_score_by_user_id(post_id,db:Session = Depends(get_db)):
    return get_all_comment_by_post_id(post_id,db)

@router.put('/update/{id}',status_code=status.HTTP_202_ACCEPTED)
async def update_comment_by_ID(id,request:CommentEdit,db:Session = Depends(get_db)):
    return update_comment_by_id(id,request,db)

@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_by_id(id,db:Session = Depends(get_db)):
    return del_comment_by_id(id,db)