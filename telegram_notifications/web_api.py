#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install aiohttp
from aiohttp import web

from add_notify import add_notify
from config import HOST, PORT
from common import TypeEnum


routes = web.RouteTableDef()


@routes.get('/')
async def index(request: web.Request):
    text = """
<form action="/add_notify" method="post" accept-charset="utf-8"
    <p>
        <label for="name">Name:</label>
        <input id="name" name="name" type="text" value="test_web_api" autofocus/>
    <p/>
    <p>
        <label for="message">Message:</label>
        <input id="message" name="message" type="message" value="BUGAGA! Привет мир!"/>
    </p>
    <input type="submit"/>
</form> 
    """

    return web.Response(text=text, content_type='text/html')


@routes.post('/add_notify')
async def add_notify_handler(request: web.Request):
    data = await request.post()
    if not data:
        data = await request.json()

    name = data['name']
    message = data['message']
    type = data.get('type', TypeEnum.INFO)
    add_notify(name, message, type)

    return web.json_response({'ok': True})


app = web.Application()
app.add_routes(routes)

web.run_app(
    app,
    host=HOST, port=PORT
)
