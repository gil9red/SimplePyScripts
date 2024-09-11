#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from fastapi import FastAPI
from db import Counter


app = FastAPI()


@app.get("/increment/{name}")
def increment(name: str) -> int:
    return Counter.increment(name)
