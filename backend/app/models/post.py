from uuid import uuid4
from xmlrpc.client import Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  Column, ForeignKey, String, Date, Float, Integer, Boolean
from sqlalchemy.orm import relationship
from ..database.init_db import Base


class Post(Base):
    __tablename__ = "post"

    post_id = Column(String(100), primary_key=True)
    post_url = Column(String(2048))
    post_date = Column(Date)
    post_profile_url = Column(String(2048))
    post_content = Column(String(2048))
    is_shared_content = Column(Boolean)
    post_reaction_count = Column(Integer)
    post_shared_count = Column(Integer)
    post_scraped_date = Column(Date)
    post_score = Column(Float)
    post_class = Column(Integer)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    user_post_owner = relationship("User", back_populates="user_contain_post")
    post_contain_comment = relationship("Comment", back_populates="post_comment_owner")
