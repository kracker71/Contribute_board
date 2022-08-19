from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import BINARY, Boolean, Column, Integer, String, Date, TypeDecorator
from sqlalchemy.orm import relationship

from app.database.init_db import Base


class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(UUID(as_uuid=True), primary_key=True,
                      index=True, default=uuid4)
    email = Column(String(50), nullable=False)
    password = Column(String(64), nullable=False)

