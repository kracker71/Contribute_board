from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  Column, String, Date, Float, Int
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
    likes = Column(Int)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    owner = relationship("User", back_populates="contain_post")
