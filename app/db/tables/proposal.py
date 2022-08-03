from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db.tables.user import User


class Proposal(Base):
    __tablename__ = "proposal"

    title = Column(String, unique=True)
    body = Column(String)
    date_created = Column(DateTime)
    creator_id = Column("User", ForeignKey("user.id"))
    #relationships
    creator = relationship(User, back_populates="proposals")

