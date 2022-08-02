from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  Column, ForeignKey, String, DateTime, Float, Integer,Text
from sqlalchemy.orm import relationship
from ..database.init_db import Base


class Comment(Base):
    __tablename__ = "comment"

    comment_id =  Column(String(100), primary_key=True)
    comment_content = Column(Text)
    comment_username = Column(String(2048))
    comment_profile_url = Column(String(2048))
    comment_date = Column(DateTime)
    comment_reaction_count = Column(Integer)
    comment_score = Column(Float)
    comment_date_scraped = Column(DateTime)
    comment_class = Column(Integer)

    user_id = Column(String(100), ForeignKey("user.user_id"))
    post_id = Column(String(100), ForeignKey("post.post_id"))
    user_comment_owner = relationship("User", back_populates="user_contain_comment")
    post_comment_owner = relationship("Post", back_populates="post_contain_comment")


