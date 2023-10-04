#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime

# pip install flask==2.3.3
from flask import Flask, render_template_string

# pip install flask-caching=2.0.2
from flask_caching import Cache


config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}

app = Flask(__name__)

# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)


@app.route("/")
@cache.cached(timeout=50)
def index():
    # SOURCE: https://stackoverflow.com/a/55050637/5909792
    return render_template_string(
        """
<html>
<head>
    <style>
    .center-screen {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      min-height: 100vh;
    }
</style>
</head>
<body>
    <div class="center-screen">
        <h1>{{ text }}</h1>
    </div>
</body>
</html>
        """,
        text=str(datetime.now()),
    )


if __name__ == "__main__":
    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=50000)

    # # Public IP
    # app.run(host='0.0.0.0')
