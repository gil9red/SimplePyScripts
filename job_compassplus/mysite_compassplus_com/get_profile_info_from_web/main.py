#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import io

# pip install flask==2.3.3
from flask import Flask, Response, abort, send_file, jsonify, url_for

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

app = Flask(__name__)

# tell Flask to use the above defined config
app.config.from_mapping(config)

CORS(app)


@app.route("/api/get_profile_image/<username>")
def api_get_profile_image(username: str):
    try:
        person: db.Person = add_or_get_db(username)
        if not person:
            abort(404)

        return send_file(io.BytesIO(person.img), mimetype="image/jpg")

    except RequestException as e:
        return Response(
            response=str(e),
            status=e.response.status_code,
        )


@app.route("/api/get_person_info/<username>")
def api_get_person_info(username: str):
    try:
        person: db.Person = add_or_get_db(username)
        if not person:
            abort(404)

        data = person.to_dict()
        # Замена байтов картинки на ее ссылку
        data["img"] = url_for(
            "api_get_profile_image",
            username=username,
            _external=True,
        )

        return jsonify(data)

    except RequestException as e:
        return Response(
            response=str(e),
            status=e.response.status_code,
        )


if __name__ == "__main__":
    from threading import Thread
    from db_updater import do_update_db
    Thread(target=do_update_db, daemon=True).start()

    app.run(
        host="0.0.0.0",
        port=50000,
        # TODO: for https
        # ssl_context=("for_https/cert.pem", "for_https/key.pem"),
    )
