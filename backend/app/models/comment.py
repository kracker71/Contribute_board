from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  Column, ForeignKey, String, Date, Float, Integer
from sqlalchemy.orm import relationship
from ..database.init_db import Base


class Comment(Base):
    __tablename__ = "comment"

    comment_id =  Column(String(100), primary_key=True)
    parent_comment_id = Column(String(100), ForeignKey("comment.comment_id"))
    comment_data = Column(String(2048))
    date_comment = Column(Date)
    comment_likes = Column(Integer)
    comment_score = Column(Float)
    
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    post_id = Column(String(100), ForeignKey("post.post_id"))
    user_comment_owner = relationship("User", back_populates="user_contain_comment")
    post_comment_owner = relationship("Post", back_populates="post_contain_comment")


