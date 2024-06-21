#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse

from market.db import NotFoundException
from market.resources import router


app = FastAPI()


@app.exception_handler(NotFoundException)
async def unicorn_exception_handler(_: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.get("/", response_class=HTMLResponse)
def index():
    return """\
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <div><a href="https://stepik.org/lesson/1186984/step/8?unit=1222202">Урок</a></div>
    <br/>
    <div><a href="/docs">/docs</a></div>
    <div><a href="/redoc">/redoc</a></div>
</body>
</html>
    """


app.include_router(router, prefix="/api/v1")
