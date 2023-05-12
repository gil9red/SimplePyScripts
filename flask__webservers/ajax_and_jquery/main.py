#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
from datetime import datetime

from flask import Flask, render_template_string, request, jsonify


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string(
        """\
<html>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-3.1.1.min.js') }}"></script>

    <body>
        <script>
            function post_method() {
                console.log("call post_method()");

                var text = $('#in_text').val();

                $.ajax({
                    url: "/post_method",
                    method: "POST",  // HTTP метод, по умолчанию GET
                    data: JSON.stringify({text: text}),

                    contentType: "application/json",
                    dataType: "json",  // тип данных загружаемых с сервера

                    success: function(data) {
                        console.log("success");
                        console.log(data);

                        $('#out_post_text').text(JSON.stringify(data));
                    },

                    error: function(data) {
                        console.log("error");
                        console.log(data);
                    }
                });
            }

            function get_method() {
                console.log("call get_method()");

                $.ajax({
                    url: "/get_method",
                    dataType: "json",  // тип данных загружаемых с сервера

                    success: function(data) {
                        console.log("success");
                        console.log(data);

                        $('#out_get_text').text(JSON.stringify(data));
                    },

                    error: function(data) {
                        console.log("error");
                        console.log(data);
                    }
                });
            }
        </script>

        <input id="in_text" type="text" value="Test data"></input>
        <button onclick="post_method();">Post!</button>
        <p id="out_post_text"></p>
        <hr><br>

        <button onclick="get_method();">Get!</button>
        <p id="out_get_text"></p>

    </body>
</html>"""
    )


@app.route("/post_method", methods=["POST"])
def post_method():
    data = request.get_json()
    print(data)

    return jsonify(data)


@app.route("/get_method")
def get_method():
    data = datetime.today()
    print(data)

    return jsonify(data)


if __name__ == "__main__":
    # Localhost
    app.debug = True
    app.run(port=10000)

    # # Public IP
    # app.run(host='0.0.0.0')
