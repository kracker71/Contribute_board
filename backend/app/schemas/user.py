from typing import List, Optional
from datetime import date
from uuid import UUID
from pydantic import BaseModel

#update_score_base
class UserBase(BaseModel):
    profile_url :str 
    
class UserRegister(UserBase):
    profile_picture_url:str
    name:str
    user_score:Optional[float] = 0    
    update_score_date:date
    
class UserEditScore(BaseModel):
    user_score:float
    update_score_date:date
    
class UserEditProfile(BaseModel):
    profile_picture_url:str
    name:str
    
class ShowUser(BaseModel):
    name:str
    profile_picture_url:str
    profile_url:str
    user_score:Optional[float] = 0 
    update_score_date:date
    class Config:
        orm_mode = True
