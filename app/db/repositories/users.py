from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.tables.user import User
from app.models import schema


class UserRepository(BaseRepository[schema.user.UserCreate, schema.user.User, User]):
    @property
    def _in_schema(self) -> Type[schema.user.UserCreate]:
        return schema.user.UserCreate

    @property
    def _schema(self) -> Type[schema.user.User]:
        return schema.user.User

    @property
    def _table(self) -> Type[User]:
        return User
