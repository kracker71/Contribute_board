from typing import List, Optional
from datetime import date
from uuid import UUID
from pydantic import BaseModel

class PostBase(BaseModel):
    post_id: str
    post_content: str
    post_url: str
    post_scraped_date: Optional[date] = None
    post_date: Optional[date] = None
    post_score:  Optional[float] = 0.0
    post_reaction_count: int
    post_profile_url:str

class PostEdit(BaseModel):
    post_data: str
    date_scrape: date
    post_score: float

class ShowPost(BaseModel):
    user_url:int
    post_url: str
    post_id: str
    post_data: str
    date_scrape: Optional[date] = None
    date_post: Optional[date] = None
    post_score:  Optional[float] = 0.0
    post_likes: int

    class Config:
        orm_mode=True
        
# class ShowAllPost(BaseModel):
#     user_url:int
#     post:List[ShowPost]
    
#     class Config:
#         orm_mode=True
    
    