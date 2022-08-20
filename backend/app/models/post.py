from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  Column, ForeignKey, String, DateTime, Float, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from ..database.init_db import Base


class Post(Base):
    __tablename__ = "post"

    post_id = Column(String(100), primary_key=True)
    post_url = Column(String(2048))
    post_date = Column(DateTime)
    post_username = Column(String(100))
    post_profile_url = Column(String(2048))
    post_content = Column(Text)
    post_shared_content = Column(Text)
    post_reaction_count = Column(Integer)
    post_comment_count = Column(Integer)
    post_shared_count = Column(Integer)
    post_score = Column(Float)
    post_scraped_date = Column(DateTime)
    post_is_update = Column(Boolean)
    post_class = Column(Integer)
    
    user_id = Column(String(100), ForeignKey("user.user_id"))
    user_post_owner = relationship("User", back_populates="user_contain_post")
    post_contain_comment = relationship("Comment", back_populates="post_comment_owner")
