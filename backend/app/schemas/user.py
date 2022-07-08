from typing import List, Optional
from datetime import date
from uuid import UUID
from pydantic import BaseModel

#update_score_base
class UserBase(BaseModel):
    user_id :str 
    
class UserRegister(UserBase):
    user_profile_picture_url:str
    user_name:str
    user_score:Optional[float] = 0    
    user_update_score_date:date
    
class UserEditScore(BaseModel):
    # user_score:float
    update_score_date:date
    
class UserEditProfile(BaseModel):
    profile_picture_url:str
    user_name:str
    
class ShowUser(BaseModel):
    user_name:str
    user_profile_picture_url:str
    user_score:Optional[float] = 0 
    user_update_score_date:date
    class Config:
        orm_mode = True
