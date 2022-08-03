from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class User(Base):
    __tablename__ = "user"
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    about = Column(String)
    profile = Column(String)
    hashed_password = Column(String)

    # relationships
    # child in one to many relationship
    # proposals = relationship("Proposal", back_populates="user")