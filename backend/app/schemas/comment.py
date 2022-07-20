from typing import List, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class CommentBase(BaseModel):
    comment_id:str
    
class CommentCreate(CommentBase):
    comment_content:Optional[str] = None
    comment_username:str
    comment_profile_url:str
    comment_date:datetime
    comment_reaction_count:Optional[int] = 0
    comment_score:Optional[float] = 0.0
    comment_date_scraped:Optional[datetime] = None

    user_id:str
    post_id:str
    
class CommentEdit(CommentBase):
    
    comment_content:Optional[str] = None
    comment_reaction_count:Optional[int] = 0
    comment_score:float
    comment_date_scraped:datetime
    
class ShowComment(BaseModel):
    
    comment_id:str
    comment_content:Optional[str] = None
    comment_username:str
    comment_profile_url:str
    comment_date:datetime
    comment_reaction_count:Optional[int] = 0
    comment_score:Optional[float] = 0.0
    comment_date_scraped:Optional[datetime] = None
    
    post_id:str
    
    class Config:
        orm_mode=True
        
# class ShowPostComment(BaseModel):
#     post_id:str
#     comment = List[ShowComment]
#     class Config:
#         orm_mode=True

# class ShowUserComment(BaseModel): 
#     user_id:UUID
#     comment = List[ShowComment]
#     class Config:
#         orm_mode=True
    