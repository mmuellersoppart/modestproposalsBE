from typing import Type
from uuid import uuid4

from passlib.context import CryptContext
from sqlalchemy import select

from app.db.repositories.base import BaseRepository
from app.db.tables.user import User
from app.db.util import row2dict
from app.models.schema import user_schema
from app.models.schema.user_schema import UserSchema, UserComplete, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    """turn passed into a hashed one"""
    return pwd_context.hash(password)

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

    async def create(self, in_schema: UserCreate) -> User:
        input_data = in_schema.dict()
        input_data['id'] = uuid4()
        input_data['hashed_password'] = get_password_hash(input_data['hashed_password'])
        entry = User(**input_data)
        self._db_session.add(entry)
        await self._db_session.commit()
        await self._db_session.refresh(entry)
        return entry

    async def get_by_username(self, username: str) -> UserComplete:
        # find user in db
        user_result = await self._db_session.execute(select(User).filter_by(username=username))
        user_result = user_result.first()[0]
        if user_result:
            return UserComplete(**row2dict(user_result))