from uuid import UUID
from app.models.schema.proposal import Proposal
from app.models.schema.base import BaseSchema


class UserBase(BaseSchema):
    username: str
    email: str
    about: str
    profile: str


class UserCreate(UserBase):
    hashed_password: str


class UserSchema(UserBase):
    id: UUID
    proposals: list[Proposal] | None


class UserPublic(UserBase):
    pass