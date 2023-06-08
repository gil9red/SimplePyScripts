#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/miguelgrinberg/flask-video-streaming/blob/599e2a582dfdde9a7d7f730518cc61a8b1fcb5de/app.py


from flask import Flask, Response, render_template_string
from camera_requests import Camera


app = Flask(__name__)


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template_string(
        """
<html>
<head>
    <title>Video Streaming Demonstration</title>
</head>
<body>
    <h1>Video Streaming Demonstration</h1>
    <img src="{{ url_for('video_feed') }}">
</body>
</html>
    """
    )


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )


@app.route("/video_feed")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        gen(Camera()),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run()
