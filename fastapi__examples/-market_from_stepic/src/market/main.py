#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from market.db import NotFoundException
from market.resources import router


app = FastAPI()


@app.exception_handler(NotFoundException)
async def unicorn_exception_handler(_: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


app.include_router(router)
