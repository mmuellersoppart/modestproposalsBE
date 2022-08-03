from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class ProposalBase(BaseModel):
    title: str
    body: str
    creator_id: UUID

class ProposalCreate(ProposalBase):
    pass

class Proposal(ProposalBase):
    id: UUID
    date_created: datetime.date
    class Config:
        orm_mode = True

