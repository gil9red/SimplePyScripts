#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import os
from datetime import date, datetime

# pip install flask==2.3.3
from flask import Flask, Response, abort, jsonify
from flask.json.provider import DefaultJSONProvider

# pip install flask-cors==4.0.0
from flask_cors import CORS

from requests.exceptions import RequestException

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


@app.route("/api/get_all_person_info/<username>")
def api_get_all_person_info(username: str) -> tuple[Response, int]:
    has_person: bool = db.Person.get_last_by_name(username) is not None

    # Проверка наличия и попытка добавить в базу для первого раза
    person: db.Person = add_or_get_db(username)
    if not person:
        abort(404)

    img_by_idx: dict[str, int] = dict()
    items: list[dict] = []

    for i, person in enumerate(db.Person.get_all(username)):
        data = person.to_dict()

        # NOTE: Картинки возвращаются в одном запросе
        data_base64 = base64.b64encode(person.img).decode("utf-8")
        img_base64 = f"data:image/jpg;base64,{data_base64}"

        # Оптимизация, чтобы не возвращать одинаковые картинки
        if img_base64 not in img_by_idx:
            img_by_idx[img_base64] = i
        else:
            img_base64 = f"={img_by_idx[img_base64]}"  # Символа "=" нет в base64

        data["img"] = img_base64

        items.append(data)

    return jsonify(items), 200 if has_person else 201


if __name__ == "__main__":
    from threading import Thread
    from db_backup import do_backup_db
    from db_updater import do_update_db

    Thread(target=do_backup_db, daemon=True).start()
    Thread(target=do_update_db, daemon=True).start()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("FLASK_PORT", 50000)),
        # TODO: for https
        # ssl_context=("for_https/cert.pem", "for_https/key.pem"),
    )
