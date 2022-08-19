from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.init_db import SessionLocal, get_db
from app.models import admin
from app.core import authentication
from app.schemas.admin import AdminAuth, AdminBase


def create(request: AdminAuth, db: Session):
    old_admin = find_by_email(request.email, db)
    if old_admin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Email is already taken")
    hashed_password = authentication.get_password_hash(request.password)
    new_admin = admin.Admin(email=request.email,
                            password=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


def find_by_email(email: str, db: Session):
    return db.query(admin.Admin).filter(admin.Admin.email == email).first()
