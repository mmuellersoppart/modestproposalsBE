import os
import time

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from app.api.routes.api import api_router
from app.api.routes.auth import oauth2_scheme
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


@app.get("/")
def main():
    return {"status": "ok"}

@app.get("/hello")
def hello(token: str = Depends(oauth2_scheme)):
    return "hello world!"