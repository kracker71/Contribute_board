from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
import datetime

#update_score_base
class UserBase(BaseModel):
    profile_picture_url:str
    name:str
    user_score:Optional[float] = 0    
    user_score_date:Optional[datetime] = 0    
    
class UserEditScore(BaseModel):
    user_score:float
    update_score_date:int
    
class UserEditProfile(BaseModel):
    profile_picture_url:str
    name:str
    