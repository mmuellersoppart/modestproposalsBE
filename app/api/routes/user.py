import logging
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.dependencies.db import get_db
from app.db.repositories.users import UserRepository
from app.models.schema import user_schema
from app.db.util import row2dict

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def list_all(
        db: AsyncSession = Depends(get_db)
) -> [user_schema.UserPublic]:
    user_repository = UserRepository(db)
    users = await user_repository.list_all()
    return [user_schema.UserPublic(**user.dict()) for user in users]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserPublic)
async def create_user(
    payload: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
) -> user_schema.UserPublic:
    user_repository = UserRepository(db)
    user = await user_repository.create(payload)
    return user_schema.UserPublic(**row2dict(user))


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=user_schema.UserPublic
)
async def create_coupon(
    user_id: UUID, db: AsyncSession = Depends(get_db)
) -> user_schema.UserPublic:
    user_repository = UserRepository(db)
    user = await user_repository.get_by_id(user_id)
    return user_schema.UserPublic(**user.dict())
