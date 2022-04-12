from fastapi import APIRouter, HTTPException, status, Depends
from app.crud.post import create_post
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.post import PostBase, PostEditScore, PostEditData

router = APIRouter(
    prefix="/post",
    tags=["Post"],
    responses={404: {"message": "Not found"}}
)


get_db = init_db.get_db


@router.post('/add_post', status_code=status.HTTP_201_CREATED)
def add_post(request: PostBase, db: Session = Depends(get_db)):
    return create_post(request, db)