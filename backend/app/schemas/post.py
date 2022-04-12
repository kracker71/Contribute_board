from datetime import date
from pydantic import BaseModel

class PostBase(BaseModel):
    post_id: str
    post_data: str
    post_url: str
    date_scrape: date
    date_post: date
    post_score: float
    post_likes: int
    
class PostEditData(BaseModel):
    post_data: str
    date_scrape: date

class PostEditScore(BaseModel):
    psot_score: float
    
    
    