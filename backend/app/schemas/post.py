from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    
    post_id: str
    post_url: str
    user_id:str
    post_is_update:Optional[bool] = False
    
class PostCreate(PostBase):
    
    post_date: datetime
    post_username:str
    post_profile_url:str
    post_content: Optional[str] = None
    post_shared_content: Optional[str] = None
    post_reaction_count: Optional[int] = 0
    post_comment_count: Optional[int] = 0
    post_shared_count: Optional[int] = 0
    post_score:  Optional[float] = 0.0
    post_scraped_date: Optional[datetime] = None
    post_is_update:Optional[bool] = False

class PostEdit(PostBase):
    post_content: Optional[str] = None
    post_shared_content: Optional[str] = None
    post_reaction_count: Optional[int] = 0
    post_comment_count: Optional[int] = 0
    post_shared_count: Optional[int] = 0
    post_score: float
    post_scraped_date: datetime
    post_is_update:Optional[bool] = False
    
class PostScoring(PostBase):
    
    post_score: float
    post_scraped_date: datetime
    post_class:Optional[int] = None

class ShowPost(BaseModel):

    post_url: str
    post_date: datetime
    post_username:str
    post_profile_url:str
    post_content: Optional[str] = None
    post_shared_content: Optional[str] = None
    post_reaction_count: Optional[int] = 0
    post_comment_count: Optional[int] = 0
    post_shared_count: Optional[int] = 0
    post_score:  Optional[float] = 0.0
    post_scraped_date: Optional[datetime] = None
    post_class:Optional[int] = None

    class Config:
        orm_mode=True
        
# class ShowAllPost(BaseModel):
#     user_url:int
#     post:List[ShowPost]
    
#     class Config:
#         orm_mode=True
    
    