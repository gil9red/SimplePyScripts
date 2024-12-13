#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from fastapi import FastAPI, Request


@dataclass
class Ip:
    host: str


app = FastAPI()


@app.get("/")
def index(request: Request) -> str:
    return request.client.host


@app.get("/json")
def index(request: Request) -> Ip:
    return Ip(
        host=request.client.host,
    )


if __name__ == "__main__":
    from pathlib import Path
    import uvicorn

    uvicorn.run(
        app=f"{Path(__file__).stem}:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
