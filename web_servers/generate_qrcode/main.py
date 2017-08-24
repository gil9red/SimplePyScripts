#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os

from flask import Flask, request, jsonify, render_template_string, send_from_directory, url_for, redirect
app = Flask(__name__)

UPLOAD_FOLDER = 'images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string('''\
<html>
    <head>
        <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
        <title>Generate QR Code</title>

        <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-3.1.1.min.js') }}"></script>
            
    </head>
    <body>
        <a href="/generate_qrcode">/generate_qrcode</a>
        <br>
        <br>
    
        <form id="form__generate_qrcode" method="post" action="/generate_qrcode">
            <b>Generate QR Code:</b><br>
            <p><textarea rows="10" cols="45" type="text" name="text" required>https://github.com/gil9red</textarea></p>
            <p><input type="submit" value="Generate"></p>
        </form>
        
        <br><br>
        <div id="block_qrcode" style="display: none">
        <a id="url_qrcode">Link</a><br>
        <a id="url_qrcode_download">Download<a><br>
        
        <img id="img_qrcode"/>
        <div>
        
        <script>
        $(document).ready(function() {
            // Обработка изменения цены конкретной игры
            $("#form__generate_qrcode").submit(function() {
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
                    success: function(data) {
                        console.log(data);
                        console.log(JSON.stringify(data));
                        
                        $('#img_qrcode').attr('src', data.file_name);
                        $('#url_qrcode').attr('href', data.file_name);
                        $('#url_qrcode_download').attr('href', data.file_name + '?download=True');
                        $('#block_qrcode').show();
                    },
                });
    
                return false;
            });
        });
        </script>
    </body>
</html>
''')


@app.route("/generate_qrcode", methods=['GET', 'POST'])
def generate_qrcode():
    text = request.args.get('text', None)
    if not text:
        text = request.form.get('text')

    download = request.args.get('download', False)
    is_redirect = request.args.get('redirect', None)

    if not text:
        return """\
        Example:<br>
        <a href="/generate_qrcode?text=Hello World!">/generate_qrcode?text=Hello World!<a><br>
        <a href="/generate_qrcode?text=Hello World!&download=True">/generate_qrcode?text=Hello World!&download=True<a><br>
        <a href="/generate_qrcode?text=Hello World!&redirect=True">/generate_qrcode?text=Hello World!&redirect=True<a><br>
        """

    import hashlib
    algo = hashlib.md5(text.encode())
    hash_data = algo.hexdigest()

    file_name = hash_data + '.png'
    upload_folder = app.config['UPLOAD_FOLDER']
    abs_file_name = os.path.join(upload_folder, file_name)

    if not os.path.exists(abs_file_name):
        # pip install qrcode
        import qrcode
        img = qrcode.make(text)
        img.save(abs_file_name)

    uri = url_for(upload_folder, file_name=file_name)

    if is_redirect:
        return redirect(uri)

    if download:
        return send_from_directory(app.config['UPLOAD_FOLDER'], file_name, as_attachment=True)

    return jsonify({
        # url_for составляет путь для функции images, которая возвращает картинку с сервера
        'file_name': uri,
    })


@app.route('/' + UPLOAD_FOLDER + '/<file_name>')
def images(file_name):
    download = request.args.get('download', False)
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_name, as_attachment=download)


if __name__ == "__main__":
    app.debug = True

    # Localhost
    app.run(
        port=5001,
        threaded=True,
    )

    # # Public IP
    # app.run(
    #     host='0.0.0.0',
    #     port=5000,
    #     threaded=True,
    # )
