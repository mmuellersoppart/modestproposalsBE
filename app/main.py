import os
import time
from datetime import datetime, timedelta

from starlette import status
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.api.dependencies.db import get_db
from app.api.routes.api import api_router
from app.core.config import settings
from app.db.tables.user import User
from app.db.util import row2dict
from app.models.schema.token_schema import TokenData, TokenSchema
from app.models.schema.user_schema import UserSchema, UserComplete

os.environ["TZ"] = settings.TIMEZONE
time.tzset()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "0c39520c4a34be395a53ff9700ab0f7cd6e8b7b9ff1cef5c8e30285cc3a75cf1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """turn passed into a hashed one"""
    return pwd_context.hash(password)

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=TokenSchema)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/")
def main():
    return {"status": "ok"}

@app.get("/hello")
def hello(token: str = Depends(oauth2_scheme)):
    return "hello world!"