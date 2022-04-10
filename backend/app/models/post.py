from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  Column, ForeignKey, String, Date, Float, Integer
from sqlalchemy.orm import relationship
from ..database.init_db import Base


class Post(Base):
    __tablename__ = "post"

    post_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    post_data = Column(String(2048))
    post_url = Column(String(2048))
    date_scrape = Column(Date)
    date_post = Column(Date)
    post_score = Column(Float)
    post_likes = Column(Integer)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    user_post_owner = relationship("User", back_populates="user_contain_post")
    post_contain_comment = relationship("Comment", back_populates="post_comment_owner")
