from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  Column, String, Date, Float
from sqlalchemy.orm import relationship
from ..database.init_db import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100))
    user_score = Column(Float)
    update_score_date = Column(Date)
    profile_picture_url = Column(String(2048))
    

    contain_post = relationship("Post", back_populates="owner")
