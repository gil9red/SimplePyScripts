#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from fastapi import FastAPI
from config import LOGGING_CONFIG


app = FastAPI()


@app.get("/")
def index():
    return {"text": "Hello World!"}


if __name__ == "__main__":
    from pathlib import Path
    import uvicorn

    uvicorn.run(
        app=f"{Path(__file__).stem}:app",
        host="127.0.0.1",
        port=8000,
        log_config=LOGGING_CONFIG,
        reload=True,
    )
