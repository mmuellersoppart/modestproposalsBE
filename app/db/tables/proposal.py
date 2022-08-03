from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Proposal(Base):
    __tablename__ = "proposal"

    title = Column(String, unique=True)
    body = Column(String)
    date_created = Column(DateTime)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    #relationships
    creator = relationship('User', backref='proposals', lazy=True)