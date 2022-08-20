from fastapi import APIRouter, HTTPException, status, Depends
from app.core.authentication import verify_password, create_access_token
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.admin import AdminAuth, AdminBase, LoginRes, Admin
from app.crud.admin import create, find_by_email

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"message": "Not found"}}
)

get_db = init_db.get_db


@router.post('/register', response_model=Admin, status_code=status.HTTP_201_CREATED)
def register(request: AdminAuth, db: Session = Depends(get_db)):
    return create(request, db)


@router.post('/login', response_model=LoginRes, status_code=status.HTTP_200_OK)
def login(request: AdminAuth, db: Session = Depends(get_db)):
    user = find_by_email(request.email, db)

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    jwt = create_access_token({"email": user.email})
    return {"token": jwt, "token_type": "bearer"}


@router.get('/', response_model=Admin, status_code=status.HTTP_200_OK)
def get_admin_by_email(email: str, db: Session = Depends(get_db)):
    return find_by_email(email, db)
