#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import time
import threading
import sys

from flask import Flask, render_template_string, request, jsonify

sys.path.append("..")
from rumble import set_vibration


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string(
        """\
<html>
    <head>
        <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
        <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-3.1.1.min.js') }}"></script>

        <!-- SOURCE: http://shpargalkablog.ru/2013/08/checked.html -->
        <style>
            #payt3 {display: none;}
            [for="payt3"] {
              position: relative;
              display: block;
              width: 100px;
              height: 100px;
              border-radius: 100%;
              background: #ddd linear-gradient(#ccc, #fff);
              box-shadow:
                    inset 0 2px 1px rgba(0,0,0,.15),
                    0 2px 5px rgba(200,200,200,.1);
              cursor: pointer;
            }
            [for="payt3"]:after {
              content: "";
              position: absolute;
              left: 40%; top: 40%;
              width: 20%;
              height: 20%;
              border-radius: 100%;
              background: #969696 radial-gradient(40% 35%, #ccc, #969696 60%);
              box-shadow:
                    inset 0 2px 4px 1px rgba(0,0,0,.3),
                    0 1px 0 rgba(255,255,255,1),
                    inset 0 1px 0 white;
            }
            [for="payt3"]:before {
              content: "";
              position: absolute;
              top: 8%; right: 8%; bottom: 8%; left: 8%;
              border-radius: 100%;
              background: #eaeaea;
              box-shadow:
                    0 3px 5px rgba(0,0,0,.25),
                    inset 0 1px 0 rgba(255,255,255,.3),
                    inset 0 -5px 5px rgba(100,100,100,.1),
                    inset 0 5px 5px rgba(255,255,255,.3);
            }
            #payt3:checked ~ [for="payt3"]:before {
              background: #e5e5e5 linear-gradient(#dedede, #fdfdfd);
            }
            #payt3:checked ~ [for="payt3"]:after {
              background: #25d025 radial-gradient(40% 35%, #5aef5a, #25d025 60%);
              box-shadow:
                    inset 0 3px 5px 1px rgba(0,0,0,.1),
                    0 1px 0 rgba(255,255,255,.4),
                    0 0 10px 2px rgba(0, 210, 0, .5);
            }
        </style>

    </head>

    <body>
        <script>
            function send_status() {
                var left_motor = $('#left_motor').val();
                var right_motor = $('#right_motor').val();

                $('#left_motor_value').text(left_motor);
                $('#right_motor_value').text(right_motor);

                var data = {
                    enabled: $('#payt3').prop('checked'),
                    left_motor: left_motor,
                    right_motor: right_motor,
                };

                console.log("data = " + JSON.stringify(data));

                $.ajax({
                    url: "/set_status",
                    method: "POST",  // HTTP метод, по умолчанию GET
                    data: JSON.stringify(data),

                    contentType: "application/json",
                    dataType: "json",  // тип данных загружаемых с сервера

                    success: function(data) {
                        console.log("success");
                        console.log(data);
                    },

                    error: function(data) {
                        console.log("error");
                        console.log(data);
                    }
                });
            }

            $(document).ready(function() {
                $.ajax({
                    url: "/get_status",

                    contentType: "application/json",
                    dataType: "json",  // тип данных загружаемых с сервера

                    success: function(data) {
                        console.log("success");
                        console.log(data);

                        $('#payt3').prop('checked', data.enabled)
                        $('#left_motor').val(data.left_motor);
                        $('#right_motor').val(data.right_motor);

                        $('#left_motor_value').text(data.left_motor);
                        $('#right_motor_value').text(data.right_motor);
                    },

                    error: function(data) {
                        console.log("error");
                        console.log(data);
                    }
                });
            });
        </script>

        <table>
            <tr>
                <td colspan="2" style="text-align: center;">Rumble / Vibration</td>
            </tr>
            <tr>
                <td colspan="2">
                    <input type="checkbox" id="payt3" oninput="send_status();"/>
                    <label align="center" for="payt3"></label>
                </td>
            </tr>
            <tr><td>Left motor:</td><td>Right motor:</td></tr>
            <tr>
                <td><input id="left_motor" type="range" min="0" max="65535" step="1" value="0" onchange="send_status();"></td>
                <td><input id="right_motor" type="range" min="0" max="65535" step="1" value="0" onchange="send_status();"></td>
            </tr>
            <tr>
                <td id="left_motor_value" style="text-align: center;">0</td>
                <td id="right_motor_value" style="text-align: center;">0</td>
            </tr>
        </table>
    </body>
</html>"""
    )


# Для отладки состояния ENABLED, LEFT_MOTOR и RIGHT_MOTOR
DEBUG = False

ENABLED = False
LEFT_MOTOR = 0
RIGHT_MOTOR = 0


@app.route("/set_status", methods=["POST"])
def set_status():
    print("set_status")

    data = request.get_json()
    print(data)

    global ENABLED, LEFT_MOTOR, RIGHT_MOTOR
    if "enabled" in data and "left_motor" in data and "right_motor" in data:
        ENABLED = data["enabled"]
        LEFT_MOTOR = int(data["left_motor"])
        RIGHT_MOTOR = int(data["right_motor"])

    return jsonify(data)


@app.route("/get_status")
def get_status():
    print("get_status")

    data = {
        "enabled": ENABLED,
        "left_motor": LEFT_MOTOR,
        "right_motor": RIGHT_MOTOR,
    }
    print(data)

    return jsonify(data)


def vibration_tick() -> None:
    while True:
        if DEBUG:
            print(
                f"ENABLED: {ENABLED} ({type(ENABLED)}), "
                f"LEFT_MOTOR: {LEFT_MOTOR}, RIGHT_MOTOR: {RIGHT_MOTOR}"
            )

        if ENABLED:
            set_vibration(LEFT_MOTOR, RIGHT_MOTOR)
        else:
            set_vibration(0, 0)

        time.sleep(0.1)


if __name__ == "__main__":
    t = threading.Thread(target=vibration_tick)
    t.start()

    # # Localhost
    # # app.debug = True
    # app.run(
    #     # OR: host='127.0.0.1'
    #     host='192.168.0.102',
    #     port=10000
    # )

    # # Public IP
    app.run(host="0.0.0.0")
