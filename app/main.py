import os
import time

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.api.routes.api import api_router
from app.core.config import settings

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

@app.get("/")
def main():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return "hello world!"