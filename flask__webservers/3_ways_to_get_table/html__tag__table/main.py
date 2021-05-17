#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import sys

from flask import Flask, render_template_string

# Для импорта common.py
sys.path.append('..')
from common import generate_table


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    items = generate_table(10)

    return render_template_string("""\
<html>
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>generate_table</title>
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-3.1.1.min.js') }}"></script>
    
    <style>
        table {
            border-spacing: 0;
        }
        
        table, th, td {
           border: solid black 1px;
        }
    
        td {
            width: 30px;
            padding: 5px;
        }
        
        tr:nth-child(1) {
            background: #cccccc;
        }
        tr > td:nth-child(1) {
            background: #cccccc;
        }
        tr:nth-child(1) > td:nth-child(1) {
            background: #ffffff;
        }
        
    </style>
</head>
<body>
    <table>
        <tbody>
            {% for row in items %}
            <tr>
                {% for item in row %}
                <td>{{ item }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
    """, items=items)


if __name__ == '__main__':
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
