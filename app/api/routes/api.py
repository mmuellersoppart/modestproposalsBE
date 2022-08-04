from fastapi import APIRouter

from app.api.routes import coupons, user

api_router = APIRouter()
api_router.include_router(coupons.router, prefix="/coupons", tags=["coupons"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
