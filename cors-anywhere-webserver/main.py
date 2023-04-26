#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from urllib.request import urlopen, Request

import flask


# TODO: append logging
app = flask.Flask(__name__)
app.debug = True


@app.route("/")
def index():
    url = flask.request.args.get("url")
    print("URL:", url)
    if not url:
        return f"Append url, please: {flask.request.host_url}?url=&lt;your_url&gt;"

    headers = dict()
    headers["Origin"] = flask.request.host_url

    request = Request(url, headers=headers)

    with urlopen(request) as f:
        content = f.read()
        print(content)

        # Нужно узнать encoding, для этого вытаскиваем xml-декларацию, а из нее уже значение encoding
        try:
            s_index = content.find(b"<?")
            e_index = content.find(b"?>")
            if s_index != -1 and e_index != -1:
                declaration = content[s_index : e_index + len(b"?>")].decode("utf-8")

                match = re.search(r'encoding="(.+)"', declaration)
                if match:
                    print(match.group(1))
                    content = content.decode(match.group(1))

        except Exception as e:
            print(e)

        headers = dict(f.getheaders())

        rs = flask.Response(content)
        rs.headers.extend(headers)
        rs.headers["Access-Control-Allow-Origin"] = "*"
        print(rs.headers)
        return rs


if __name__ == "__main__":
    # Localhost
    app.run()

    # # Public IP
    # app.run(host='0.0.0.0')
