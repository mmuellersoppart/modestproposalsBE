import os
import time

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.dependencies.db import get_db
from app.api.routes.api import api_router
from app.core.config import settings
from app.db.tables.user import User
from app.db.util import row2dict
from app.models.schema.user_schema import UserSchema, UserComplete

os.environ["TZ"] = settings.TIMEZONE
time.tzset()


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        debug=settings.DEBUG,
    )
    application.include_router(api_router, prefix=settings.API_V1_STR)
    return application


app = get_application()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_hash_password(password: str):
    return "fakehashed" + password


async def get_user(db, username: str):

    # find user in db
    user_result = await db.execute(select(User).filter_by(username=username))
    user_result = user_result.first()[0]
    if user_result:
        return UserComplete(**row2dict(user_result))

async def fake_decode_token(db, token):
    """
    Intake the token and return the correct person.
    """
    # This doesn't provide any security at all
    # Check the next version
    user = await get_user(db, token)
    return user

async def get_current_active_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = await fake_decode_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.post("/token")
async def login(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user_result = await db.execute(select(User).where(User.username == form_data.username))
    user_result = user_result.first()[0]
    if not user_result:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = UserComplete(**row2dict(user_result))
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/")
def main():
    return {"status": "ok"}

@app.get("/hello")
def hello(token: str = Depends(oauth2_scheme)):
    return "hello world!"