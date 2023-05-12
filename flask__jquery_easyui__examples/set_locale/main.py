#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://www.jeasyui.com/tutorial/index.php
# SOURCE: http://www.jeasyui.com/tutorial/app/crud.php


import logging
from flask import Flask, render_template_string


app = Flask(__name__, static_folder="../static")
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string(
        """\
<html>
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>set_locale</title>

    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='js/jquery-easyui-1.6.3/themes/default/easyui.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='js/jquery-easyui-1.6.3/themes/icon.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='js/jquery-easyui-1.6.3/themes/color.css') }}">
    
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-easyui-1.6.3/jquery.min.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-easyui-1.6.3/jquery.easyui.min.js') }}"></script>
    
    <!-- VARIANT 1 -->
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-easyui-1.6.3/locale/easyui-lang-ru.js') }}"></script>
</head>
<body>
    <!-- VARIANT 2 -->
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-easyui-1.6.3/easyloader.js') }}"></script>
    <script type="text/javascript">
        $('document').ready(function() {
            easyloader.locale = 'ru';
        });
    </script>

    <div class="easyui-calendar" style="width:250px;height:250px;"></div>
</body>
</html>
    """
    )


if __name__ == "__main__":
    # app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
