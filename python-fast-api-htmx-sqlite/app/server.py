from fastapi import Depends, FastAPI, Request, Response, Security, Path
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_sso.sso.google import GoogleSSO
from fastapi.security import APIKeyCookie
from fastapi_sso.sso.base import OpenID
from starlette import status
from starlette.exceptions import HTTPException
from fastapi.exception_handlers import http_exception_handler
import datetime


from jose import jwt

import sys

sys.path.append("./database")
sys.path.append(".")

from database.database import (
    AsyncDatabase,
    DatabaseException,
    DatabaseExceptionType as db_e_type,
)
from database.models import (
    Example
)
from config import Config
from logger import Logger, RequestSpan

# Constants


# App State

try:
    CONFIG = Config()
    print("DATABASE_PATH: ", CONFIG.database_path)
    print("LOG_PATH: ", CONFIG.log_path)
    print("HOST_NAME: ", CONFIG.host_name)
    print("LISTEN_ADDRESS: ", CONFIG.listen_address)
    print("LISTEN_PORT: ", CONFIG.listen_port)

    DATABASE = AsyncDatabase(CONFIG.database_path)
    LOGGER = Logger(CONFIG.log_path, CONFIG.debug)
    APP = FastAPI()
except Exception as e:
    print("Error setting up APP: ", e)
    exit(1)


# Exceptions


@APP.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_403_FORBIDDEN and request.scope[
        "path"
    ].startswith("/app"):
        return RedirectResponse(url="/app/login")
    elif exc.status_code == status.HTTP_401_UNAUTHORIZED and request.scope[
        "path"
    ].startswith("/app"):
        return RedirectResponse(url="/app/login")
    # Instead of calling itself, return a JSON response
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# Middleware


@APP.middleware("http")
async def async_db_middleware(request: Request, call_next):
    try:
        async with DATABASE.AsyncSession() as session:
            request.state.db = session
            response = await call_next(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e
    finally:
        await request.state.db.close()
    return response


@APP.middleware("http")
async def span_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.span = LOGGER.get_request_span(request)
        response = await call_next(request)
    finally:
        pass
    return response


# Dependencies

def async_db(request: Request):
    return request.state.db


def span(request: Request):
    return request.state.span

# HTML ROUTES

## HOME PAGE ROUTES

home_templates = Jinja2Templates(directory="templates/home")


### Index Page


@APP.get("/", response_class=HTMLResponse)
def home_index(request: Request):
    # Check if htmx request
    if request.headers.get("HX-Request"):
        return home_templates.TemplateResponse(
            "index_content.html", {"request": request}
        )
    return home_templates.TemplateResponse("index.html", {"request": request})


# TODO: unique page content
### About Page


@APP.get("/about", response_class=HTMLResponse)
def home_about(request: Request):
    # Check if htmx request
    if request.headers.get("HX-Request"):
        return home_templates.TemplateResponse(
            "index_content.html", {"request": request}
        )
    return home_templates.TemplateResponse("index.html", {"request": request})


### Blog Page


@APP.get("/blog", response_class=HTMLResponse)
def home_blog(request: Request):
    # Check if htmx request
    if request.headers.get("HX-Request"):
        return home_templates.TemplateResponse(
            "index_content.html", {"request": request}
        )
    return home_templates.TemplateResponse("index.html", {"request": request})


### Contact Page


@APP.get("/contact", response_class=HTMLResponse)
def home_contact(request: Request):
    # Check if htmx request
    if request.headers.get("HX-Request"):
        return home_templates.TemplateResponse(
            "index_content.html", {"request": request}
        )
    return home_templates.TemplateResponse("index.html", {"request": request})


# Static Files

APP.mount("/static", StaticFiles(directory="static"), name="static")

# API Routes

API_VERSION = "v0"
API_PATH = f"api/{API_VERSION}"

# Hello

@APP.get(f"/{API_PATH}/hello")
async def hello():
    return {"message": "Hello World"}

# Run

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(APP, host=CONFIG.listen_address, port=CONFIG.listen_port,  proxy_headers=True)
