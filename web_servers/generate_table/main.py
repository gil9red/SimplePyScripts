#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, render_template_string
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    N = 20
    items = [[str(i) for i in range(N + 1)]]

    for i in range(1, N + 1):
        row = [str(i)]

        for j in range(1, N + 1):
            row.append(str(i * j))

        items.append(row)

    items[0][0] = ''

    return render_template_string("""\
<!DOCTYPE html>
<html lang="ru">
<head>
    <title>generate_table</title>
    
    <style>
        td {
            width: 30px;
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
    <table cellspacing="0" border="1" cellpadding="5">
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

    # :param threaded: should the process handle each request in a separate
    #                  thread?
    # :param processes: if greater than 1 then handle each request in a new process
    #                   up to this maximum number of concurrent processes.
    app.threaded = True

    # Localhost
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
