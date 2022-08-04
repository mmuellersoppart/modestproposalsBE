from unittest import mock

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.repositories.users import UserRepository
from app.models.schema.user_schema import UserCreate

pytestmark = pytest.mark.asyncio


async def test_user_create(
    async_client: AsyncClient, db_session: AsyncSession
) -> None:
    user_repository = UserRepository(db_session)
    payload = {
      "username": "u2",
      "email": "u2@m.com",
      "about": "Hi I am u2.",
      "profile": "blue2",
      "hashed_password": "u1secret"
    }

    response = await async_client.post("/v1/users/", json=payload)
    user = await user_repository.get_by_id(response.json()["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
      "username": "u2",
      "email": "u2@m.com",
      "about": "Hi I am u2.",
      "profile": "blue2",
        "id": str(user.id),
    }


# async def test_coupon_get_by_id(
#     async_client: AsyncClient, db_session: AsyncSession
# ) -> None:
#     payload = {
#         "code": "PIOTR",
#         "init_count": 100,
#     }
#     user_repository = CouponsRepository(db_session)
#     coupon = await user_repository.create(InCouponSchema(**payload))
#
#     response = await async_client.get(f"/v1/user/{coupon.id}")
#
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == {
#         "code": payload["code"],
#         "init_count": payload["init_count"],
#         "remaining_count": payload["init_count"],
#         "id": mock.ANY,
#     }
