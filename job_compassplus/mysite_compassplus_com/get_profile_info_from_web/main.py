#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import io
import os
from datetime import date, datetime

# pip install flask==2.3.3
from flask import Flask, Response, abort, send_file, jsonify, url_for
from flask.json.provider import DefaultJSONProvider

# pip install flask-cors==4.0.0
from flask_cors import CORS

from requests.exceptions import RequestException
from peewee import DoesNotExist

import db
from db_updater import add_or_get_db


config = {
    # "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}


class UpdatedJSONProvider(DefaultJSONProvider):
    sort_keys = False

    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        return super().default(o)


app = Flask(__name__)

# Tell Flask to use the above defined config
app.config.from_mapping(config)

app.json = UpdatedJSONProvider(app)

CORS(app)


@app.errorhandler(RequestException)
def handle_requests_error(e: RequestException) -> Response:
    return Response(
        response=str(e),
        status=e.response.status_code if e.response else 404,
    )


def get_response_jpg(img: bytes) -> Response:
    return send_file(io.BytesIO(img), mimetype="image/jpg")


@app.route("/api/get_profile_image/<username>")
def api_get_profile_image(username: str):
    person: db.Person = add_or_get_db(username)
    if not person:
        abort(404)

    return get_response_jpg(person.img)


@app.route("/api/get_profile_image_by_id/<int:person_id>")
def api_get_profile_image_by_id(person_id: int):
    try:
        person: db.Person = db.Person.get_by_id(person_id)
    except DoesNotExist:
        abort(404)

    return get_response_jpg(person.img)


@app.route("/api/get_all_person_info/<username>")
def api_get_all_person_info(username: str):
    # Проверка наличия и попытка добавить в базу для первого раза
    person: db.Person = add_or_get_db(username)
    if not person:
        abort(404)

    items = []
    for person in db.Person.get_all(username):
        data = person.to_dict()

        # Ссылка на картинку
        data["img"] = url_for(
            "api_get_profile_image_by_id",
            person_id=person.id,
            _external=True,
        )

        items.append(data)

    return jsonify(items)


if __name__ == "__main__":
    from threading import Thread
    from db_updater import do_update_db
    Thread(target=do_update_db, daemon=True).start()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("FLASK_PORT", 50000)),
        # TODO: for https
        # ssl_context=("for_https/cert.pem", "for_https/key.pem"),
    )
