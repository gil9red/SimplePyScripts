#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import base64
import logging
import io

import requests

from flask import Flask, jsonify, render_template_string, redirect, request
from PIL import Image

# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/4516206d6e29608a732b7c096cd557b11c7ce67b/telegram_bot__image_process_bot/commands.py
from commands import invert, gray, invert_gray, pixelate, jackal_jpg, thumbnail, blur


COMMANDS = {
    'invert': invert,
    'gray': gray,
    'invert_gray': invert_gray,
    'pixelate': pixelate,
    'pixelate16': lambda img: pixelate(img, 16),
    'pixelate32': lambda img: pixelate(img, 32),
    'pixelate48': lambda img: pixelate(img, 48),
    'jackal_jpg': jackal_jpg,
    'thumbnail32': lambda img: thumbnail(img, (32, 32)),
    'thumbnail64': lambda img: thumbnail(img, (64, 64)),
    'thumbnail128': lambda img: thumbnail(img, (128, 129)),
    'blur': blur,
    'blur5': lambda img: blur(img, 5)
}


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/master/img_to_base64_html/main.py
def img_to_base64_html(file_name__or__bytes__or__file_object):
    arg = file_name__or__bytes__or__file_object

    if type(arg) == str:
        with open(arg, mode='rb') as f:
            img_bytes = f.read()

    elif type(arg) == bytes:
        img_bytes = arg

    else:
        img_bytes = arg.read()

    bytes_io = io.BytesIO(img_bytes)
    img = Image.open(bytes_io)

    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    # print(img_base64)

    return 'data:image/{};base64,'.format(img.format.lower()) + img_base64


app = Flask(__name__)

# http://flask.pocoo.org/docs/0.12/config/#config
# By default Flask will serialize JSON objects in a way that the keys are ordered. This is done in order to
# ensure that independent of the hash seed of the dictionary the return value will be consistent to not trash external
# HTTP caches. You can override the default behavior by changing this variable. This is not recommended but might give
# you a performance improvement on the cost of cacheability.
app.config['JSON_SORT_KEYS'] = False

logging.basicConfig(level=logging.DEBUG)


LAST_IMAGE = 'last_image.jpg'


def save_last_image(file_data):
    with open(LAST_IMAGE, 'wb') as f:
        f.write(file_data)


def load_last_image():
    with open(LAST_IMAGE, 'rb') as f:
        return f.read()


@app.route('/')
def index():
    return render_template_string('''\
<html>
    <head>
        <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
        <title>get_upload_and_image_process</title>

        <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-3.1.1.min.js') }}"></script>
        
    </head>
    <body>
        <p>get_upload_image_info:</p>
        <table>
            <tr>
                <td>
                    <form class="form__upload_file" action="/upload_file" method="post" enctype="multipart/form-data">
                        <label>Image file: <input type="file" name="file" accept="image/*"></label>
                        <p><input value="OK" type="submit"></p>
                    </form>
                </td>
                <td><div style="width: 100px;"></div></td>
                <td>
                    <form class="form__upload_url" action="/upload_url" method="post" enctype="multipart/form-data">
                        <label>Image url: <input type="url" name="url" onkeydown="this.style.width = ((this.value.length + 1) * 8) + 'px';"></label>
                        <p><input value="OK" type="submit"></p>
                    </form>
                </td>
            </tr>
        </table>

        <div class="block progress" style="display: none">
            <p>Пожалуйста, подождите, файл загружаются.</p>
            <progress class="progress upload" max="100" value="0"></progress>
        </div>

        <div class="result show" style="display: none">
            <form class="form__image_process" action="/image_process" method="post" enctype="multipart/form-data">
                <p>Выберите команду: 
                <select name="command"> 
                   {% for key in commands %}
                      <option value="{{ key }}">{{ key }}</option>
                   {% endfor %}
                </select>
                <input value="OK" type="submit">
                </p>
            </form>
                    
            <table>
                <capture>Результат от сервера:</capture>
                <tr>
                    <th>ORIGINAL</th><th>PROCESS</th>
                </tr>
                <tr>
                    <td><img class="original" width="400px" height="400px" alt="image original"/></td>
                    <td><img class="process" width="400px" height="400px" alt="image process"/></td>
                </tr>
            </table>
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
            
            function on_success(data) {
                console.log(data);
                $('.block.progress').hide();
                $('.result.show').show();
                    
                $('img.original').attr('src', data.img_original);
                $('img.process').attr('src', data.img_process);
            }
        
            $(".form__upload_file").submit(function() {
                $('.block.progress').show();
                $('.result.show').hide();

                var thisForm = this;

                var url = $(this).attr("action");
                var method = $(this).attr("method");
                if (method === undefined) {
                    method = "get";
                }
                
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

                    success: on_success,
                });

                return false;
            });
            
            $(".form__upload_url").submit(function() {
                $('.block.progress').show();
                $('.result.show').hide();

                var thisForm = this;

                var url = $(this).attr("action");
                var method = $(this).attr("method");
                if (method === undefined) {
                    method = "get";
                }

                var data = $(this).serialize();

                $.ajax({
                    url: url,
                    method: method,  // HTTP метод, по умолчанию GET
                    data: data,
                    dataType: "json",  // тип данных загружаемых с сервера

                    xhr: function() {
                        var myXhr = $.ajaxSettings.xhr();
                        if (myXhr.upload) {
                            myXhr.upload.addEventListener('progress', progress, false);
                        }

                        return myXhr;
                    },

                    success: on_success,
                });

                return false;
            });
            
            $(".form__image_process").submit(function() {
                $('.block.progress').show();
                $('.result.show').hide();

                var thisForm = this;

                var url = $(this).attr("action");
                var method = $(this).attr("method");
                if (method === undefined) {
                    method = "get";
                }

                var data = $(this).serialize();

                $.ajax({
                    url: url,
                    method: method,  // HTTP метод, по умолчанию GET
                    data: data,
                    dataType: "json",  // тип данных загружаемых с сервера

                    xhr: function() {
                        var myXhr = $.ajaxSettings.xhr();
                        if (myXhr.upload) {
                            myXhr.upload.addEventListener('progress', progress, false);
                        }

                        return myXhr;
                    },

                    success: on_success,
                });

                return false;
            });
        });
        </script>
    </body>
</html>
''', commands=COMMANDS)


@app.route("/upload_file", methods=['POST'])
def upload_file():
    print(request.files)

    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect('/')

    file = request.files['file']
    file_data = file.stream.read()

    save_last_image(file_data)

    return jsonify({
        'img_original': img_to_base64_html(file_data),
        'img_process': None,
    })


@app.route("/upload_url", methods=['POST'])
def upload_url():
    print(request.form)

    if 'url' not in request.form:
        return redirect('/')

    url = request.form['url']
    file_data = requests.get(url).content

    save_last_image(file_data)

    return jsonify({
        'img_original': img_to_base64_html(file_data),
        'img_process': None,
    })


@app.route("/image_process", methods=['POST'])
def image_process():
    print(request.form)
    command = request.form['command']

    img_original = load_last_image()
    data_io = io.BytesIO(img_original)
    img = Image.open(data_io).convert('RGB')

    # Получение и вызов функции
    result = COMMANDS[command](img)

    data_io = io.BytesIO()
    result.save(data_io, 'JPEG')

    img_process = data_io.getvalue()

    return jsonify({
        'img_original': img_to_base64_html(img_original),
        'img_process': img_to_base64_html(img_process),
    })


if __name__ == '__main__':
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
