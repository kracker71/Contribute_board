from typing import List, Optional
from datetime import date
from uuid import UUID
from pydantic import BaseModel

class CommentBase(BaseModel):
    comment_id:str
    
class CommentCreate(CommentBase):
    comment_data:str
    date_comment:date
    comment_like:Optional[int] = 0
    comment_score:Optional[float] = 0.0
    user_url:str
    post_url:str
    
class CommentEdit(CommentBase):
    comment_data:str
    date_comment:date
    comment_like:Optional[int] = 0
    comment_score:float
    
class ShowComment(BaseModel):
    user_id:UUID
    comment_id:str
    comment_score:float
    date_comment:date
    comment_like:Optional[int] = 0
    comment_data:str
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
    