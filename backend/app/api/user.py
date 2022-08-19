from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.user import ShowUser, UserRegister,UserEditScore, UserEditProfile
from app.schemas.post import ShowPost
from app.schemas.comment import ShowComment
from app.crud.user import (
    create_user, 
    get_user_by_id, 
    get_score_by_name, 
    get_score_by_ranking,
    update_user_profile_by_id, 
    update_user_score_by_id, 
    del_user_by_id, 
    get_all_user, 
    update_all_user_score,
    get_posts_by_user_id, 
    get_user_posts_score,
    get_comments_by_user_id,
    get_user_comments_score,
)
from app.core.authentication import validate_token
# from app.main import oauth2_scheme
router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"message": "Not found"}}
)
get_db = init_db.get_db

@router.post("/create",response_model=ShowUser,status_code=status.HTTP_201_CREATED)
async def user_create(request:UserRegister,db:Session = Depends(get_db),token = Depends(validate_token)):
    return create_user(request,db)

@router.get("/all",response_model=List[ShowUser])
async def get_all_User(db:Session = Depends(get_db)):
    return get_all_user(db)

@router.get("/{id}",response_model=ShowUser)
async def get_user_by_ID(id,db:Session = Depends(get_db)):
    return get_user_by_id(id,db)

@router.get("/score/name",response_model=List[ShowUser])
async def get_score_by_Name(db:Session = Depends(get_db)):
    return get_score_by_name(db)

@router.get("/score/ranking",response_model=List[ShowUser])
async def get_score_by_Rank(db:Session = Depends(get_db)):
    return get_score_by_ranking(db)

@router.put("/update/score/all",status_code=status.HTTP_202_ACCEPTED)
async def update_all_user_Score(request:UserEditScore,db :Session = Depends(get_db),token = Depends(validate_token)):
    return update_all_user_score(request,db)

@router.put("/update/score/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_score_by_ID(id,request:UserEditScore,db :Session = Depends(get_db),token = Depends(validate_token)):
    return update_user_score_by_id(id,request,db)

@router.put("/update/profile/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_profile_by_ID(id,request:UserEditProfile,db :Session = Depends(get_db)):
    return update_user_profile_by_id(id,request,db)

@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(id,db:Session = Depends(get_db),token = Depends(validate_token)):
    return del_user_by_id(id,db)

#####post section#####

@router.get('/post/{user_url}',response_model=List[ShowPost])
async def get_posts_by_user_ID(user_url,db:Session = Depends(get_db)):
    return get_posts_by_user_id(user_url,db)

@router.get('/post/score/{user_url}')
async def get_user_all_post_score(user_url,db:Session = Depends(get_db)):
    return get_user_posts_score(user_url,db)

#####comment section#####

@router.get('/comment/{user_url}',response_model=List[ShowComment])
async def get_comment_by_user_ID(user_url,db:Session = Depends(get_db)):
    return get_comments_by_user_id(user_url,db)

@router.get('/comment/score/{id}')
async def get_user_all_comment_score(id,db:Session = Depends(get_db)):
    return get_user_comments_score(id,db)