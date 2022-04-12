from typing import List, Optional
from datetime import date
from pydantic import BaseModel

class PostBase(BaseModel):
    post_id: str
    post_data: str
    post_url: str
    date_scrape: Optional[date] = None
    date_post: Optional[date] = None
    post_score:  Optional[float] = 0.0
    post_likes: int

    
class PostEditData(BaseModel):
    post_data: str
    date_scrape: date

class PostEditScore(BaseModel):
    psot_score: float
    
    
    