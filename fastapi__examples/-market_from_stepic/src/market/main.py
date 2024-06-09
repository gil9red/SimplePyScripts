#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from fastapi import FastAPI
from market.resources import router


app = FastAPI()
app.include_router(router)
