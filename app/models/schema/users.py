from uuid import UUID
from app.models.schema.proposal import Proposal
from app.models.schema.base import BaseSchema


class UserBase(BaseSchema):
    username: str
    email: str
    about: str
    profile: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID
    proposals: list[Proposal]

