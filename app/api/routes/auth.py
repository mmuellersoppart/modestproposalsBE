import logging
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.dependencies.db import get_db
from app.db.repositories.user import UserRepository
from app.db.tables.user import User
from app.models.schema.token_schema import TokenSchema, TokenData

router = APIRouter()
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "0c39520c4a34be395a53ff9700ab0f7cd6e8b7b9ff1cef5c8e30285cc3a75cf1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """turn passed into a hashed one"""
    return pwd_context.hash(password)


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user_repository = UserRepository(db)
    user = await user_repository.get_by_username(username)
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

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_repository = UserRepository(db)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await user_repository.get_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=TokenSchema)
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


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user