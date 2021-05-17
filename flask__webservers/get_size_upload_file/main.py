#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import sys

from flask import Flask, request, redirect, render_template_string, jsonify

sys.path.append('..')
from common import sizeof_fmt


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template_string('''\
<html>
    <head>
        <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
        <title>get_size_upload_file</title>

        <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-3.1.1.min.js') }}"></script>

    </head>
    <body>
        <br>
        <form id="form__upload_file" action="/get_file_size" method="post" enctype="multipart/form-data">
            <p>Узнайте размер файла:</p>
            <p><input type="file" name="file"></p>
            <p><input type="submit"></p>
        </form>
        <br><br>

        <div id="info" style="display: none">
            <div id="show_size" style="display: inline-block;"></div><div style="display: inline-block;">&nbsp;Bytes</div>
            <div id="show_size_human"></div>
        </div>

        <script>
        $(document).ready(function() {
            $("#form__upload_file").submit(function() {
                var thisForm = this;

                var url = $(this).attr("action");
                var method = $(this).attr("method");
                if (method === undefined) {
                    method = "get";
                }

                // var data = $(this).serialize();
                //
                // For send file object:
                var input = $("#form__upload_file > input[type=file]");
                var data = new FormData(thisForm);

                $.ajax({
                    url: url,
                    method: method,  // HTTP метод, по умолчанию GET
                    data: data,
                    dataType: "json",  // тип данных загружаемых с сервера

                    // Без этих опций неудастся передать файл
                    processData: false,
                    contentType: false,

                    success: function(data) {
                        console.log(data);
                        console.log(JSON.stringify(data));

                        $('#show_size').text(data.length);
                        $('#show_size_human').text(data.length_human);

                        $('#info').show();
                    },
                });

                return false;
            });
        });
        </script>
    </body>
</html>
''')


@app.route('/get_file_size', methods=['POST'])
def get_file_size():
    print(request.files)

    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect('/')

    length = 0

    file = request.files['file']
    if file:
        data = file.stream.read()
        length = len(data)

    return jsonify({'length': length, 'length_human': sizeof_fmt(length)})


if __name__ == '__main__':
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
