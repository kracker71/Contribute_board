from typing import List, Optional
from datetime import date
from pydantic import BaseModel

#update_score_base
class UserBase(BaseModel):
    user_id :str 
    
class UserRegister(UserBase):
    
    user_name:str
    user_profile_url:str
    user_profile_picture_url:Optional[str]=None
    user_score:Optional[float] = 0    
    user_update_score_date:date
     
class UserEditScore(BaseModel):
    
    user_score:float
    update_score_date:date
    
class UserEditProfile(BaseModel):
    
    user_name:Optional[str]=None
    profile_picture_url:Optional[str]=None
    
class ShowUser(BaseModel):
    
    user_name:str
    user_profile_picture_url:Optional[str]=None
    user_score:Optional[float] = 0 
    user_update_score_date:Optional[date] = None
    class Config:
        orm_mode = True
