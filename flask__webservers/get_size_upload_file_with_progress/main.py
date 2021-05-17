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
        <form class="form__upload_file" action="/get_file_size" method="post" enctype="multipart/form-data">
            <p>Узнайте размер файла:</p>
            <p><input type="file" name="file"></p>
            <p><input type="submit"></p>
        </form>
        
        <div class="block progress" style="display: none">
            <p>Пожалуйста, подождите, файл загружаются.</p>
            <progress class="progress upload" max="100" value="0"></progress>
        </div>
        
        <br><br>

        <div class="info size" style="display: none">
            <div class="show_size" style="display: inline-block;"></div><div style="display: inline-block;">&nbsp;Bytes</div>
            <div class="show_size_human"></div>
        </div>

        <script>
        $(document).ready(function() {
            function progress(e) {
                if(e.lengthComputable) {
                    var max = e.total;
                    var current = e.loaded;
            
                    var percentage = (current * 100) / max;
                    console.log(percentage);
                    $('.progress.upload').val(percentage);
                }  
            }
        
            $(".form__upload_file").submit(function() {
                $('.block.progress').show();
                $('.info.size').hide();
            
                var thisForm = this;

                var url = $(this).attr("action");
                var method = $(this).attr("method");
                if (method === undefined) {
                    method = "get";
                }

                // var data = $(this).serialize();
                //
                // For send file object:
                var input = $(".form__upload_file > input[type=file]");
                var data = new FormData(thisForm);

                $.ajax({
                    url: url,
                    method: method,  // HTTP метод, по умолчанию GET
                    data: data,
                    dataType: "json",  // тип данных загружаемых с сервера

                    // Без этих опций неудастся передать файл
                    processData: false,
                    contentType: false,

                    xhr: function() {
                        var myXhr = $.ajaxSettings.xhr();
                        if (myXhr.upload) {
                            myXhr.upload.addEventListener('progress', progress, false);
                        }
                        
                        return myXhr;
                    },
                    cache:false,

                    success: function(data) {
                        console.log(data);
                        console.log(JSON.stringify(data));

                        $('.info.size > .show_size').text(data.length);
                        $('.info.size > .show_size_human').text(data.length_human);

                        $('.block.progress').hide();
                        $('.info.size').show();
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
