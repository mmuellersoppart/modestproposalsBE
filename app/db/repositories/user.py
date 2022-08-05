from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.tables.user import User
from app.models.schema import user_schema


class UserRepository(BaseRepository[user_schema.UserCreate, user_schema.UserSchema, User]):
    @property
    def _in_schema(self) -> Type[user_schema.UserCreate]:
        return user_schema.UserCreate

    @property
    def _schema(self) -> Type[user_schema.UserSchema]:
        return user_schema.UserSchema

    @property
    def _table(self) -> Type[User]:
        return User
