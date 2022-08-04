from uuid import UUID
from app.models.schema.proposal_schema import ProposalSchema
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
    proposals: list[ProposalSchema] | None


class UserPublic(UserBase):
    id: UUID