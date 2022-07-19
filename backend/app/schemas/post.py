from typing import List, Optional
from datetime import date
from pydantic import BaseModel

class PostBase(BaseModel):
    
    post_id: str
    post_url: str
    
class PostCreate(PostBase):
    
    post_date: date
    post_username:str
    post_profile_url:str
    post_content: Optional[str] = None
    post_shared_content: Optional[str] = None
    post_reaction_count: Optional[int] = 0
    post_comment_count: Optional[int] = 0
    post_shared_count: Optional[int] = 0
    post_score:  Optional[float] = 0.0
    post_scraped_date: Optional[date] = None
    
    user_id:str

class PostEdit(PostBase):
    post_content: Optional[str] = None
    post_shared_content: Optional[str] = None
    post_reaction_count: Optional[int] = 0
    post_comment_count: Optional[int] = 0
    post_shared_count: Optional[int] = 0
    post_score: float
    post_scraped_date: date
    
class PostScoring(PostBase):
    
    post_score: float
    post_scraped_date: date
    post_class:Optional[int] = None

class ShowPost(BaseModel):

    post_url: str
    post_date: date
    post_username:str
    post_profile_url:str
    post_content: Optional[str] = None
    post_shared_content: Optional[str] = None
    post_reaction_count: Optional[int] = 0
    post_comment_count: Optional[int] = 0
    post_shared_count: Optional[int] = 0
    post_score:  Optional[float] = 0.0
    post_scraped_date: Optional[date] = None
    post_class:Optional[int] = None

    class Config:
        orm_mode=True
        
# class ShowAllPost(BaseModel):
#     user_url:int
#     post:List[ShowPost]
    
#     class Config:
#         orm_mode=True
    
    