#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Any
from fastapi import FastAPI
from api_search import search_game


app = FastAPI()


@app.get("/search-game/{name}")
def index(name: str) -> dict[str, Any] | None:
    return search_game(name)


if __name__ == "__main__":
    from pathlib import Path
    import uvicorn

    uvicorn.run(
        app=f"{Path(__file__).stem}:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
