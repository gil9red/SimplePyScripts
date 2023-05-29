#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import io
import json
import logging

# pip install exifread
import exifread

import requests

from flask import Flask, jsonify, render_template_string, redirect, request

# pip install humanize
from humanize import naturalsize as sizeof_fmt

from PIL import Image


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/master/print_exif/main.py
def get_exif_tags(file_object_or_file_name, as_category=True):
    if type(file_object_or_file_name) == str:
        # Open image file for reading (binary mode)
        file_object_or_file_name = open(file_object_or_file_name, mode="rb")

    # Return Exif tags
    tags = exifread.process_file(file_object_or_file_name)
    tags_by_value = dict()

    if not tags:
        # print('Not tags')
        return tags_by_value

    # print('Tags ({}):'.format(len(tags)))

    for tag, value in tags.items():
        # Process value
        try:
            if value.field_type == 1:
                try:
                    # If last 2 items equals [0, 0]
                    if value.values[-2:] == [0, 0]:
                        value = bytes(value.values[:-2]).decode("utf-16")
                    else:
                        value = bytes(value.values).decode("utf-16")

                except:
                    value = str(value.values)
            else:
                value = value.printable

            value = value.strip()

        except:
            # Example tag JPEGThumbnail
            if type(value) == bytes:
                value = base64.b64encode(value).decode()

        # print('  "{}": {}'.format(tag, value))

        if not as_category:
            tags_by_value[tag] = value

        else:
            # Fill categories_by_tag
            if " " in tag:
                category, sub_tag = tag.split(" ", maxsplit=1)

                if category not in tags_by_value:
                    tags_by_value[category] = dict()

                tags_by_value[category][sub_tag] = value

            else:
                tags_by_value[tag] = value

    # print()

    return tags_by_value


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/master/img_to_base64_html/main.py
def img_to_base64_html(file_name__or__bytes__or__file_object):
    arg = file_name__or__bytes__or__file_object

    if type(arg) == str:
        with open(arg, mode="rb") as f:
            img_bytes = f.read()

    elif type(arg) == bytes:
        img_bytes = arg

    else:
        img_bytes = arg.read()

    bytes_io = io.BytesIO(img_bytes)
    img = Image.open(bytes_io)

    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    # print(img_base64)

    return f"data:image/{img.format.lower()};base64,{img_base64}"


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/84651cfefaee768851170ec4ba7d025bbaae622d/get_image_info/main.py#L84
def get_image_info(file_name__or__bytes__or__bytes_io, pretty_json_str=False):
    data = file_name__or__bytes__or__bytes_io
    type_data = type(data)

    # File name
    if type_data == str:
        with open(data, mode="rb") as f:
            data = f.read()

    if type(data) == bytes:
        data = io.BytesIO(data)

    length = len(data.getvalue())
    exif = get_exif_tags(data)

    img = Image.open(data)

    info = dict()
    info["length"] = dict()
    info["length"]["value"] = length
    info["length"]["text"] = sizeof_fmt(length)

    info["format"] = img.format
    info["mode"] = img.mode
    info["channels"] = len(img.getbands())
    info["bit_color"] = {
        "1": 1,
        "L": 8,
        "P": 8,
        "RGB": 24,
        "RGBA": 32,
        "CMYK": 32,
        "YCbCr": 24,
        "I": 32,
        "F": 32,
    }[img.mode]

    info["size"] = dict()
    info["size"]["width"] = img.width
    info["size"]["height"] = img.height

    info["exif"] = exif

    if pretty_json_str:
        info = json.dumps(info, indent=4, ensure_ascii=False)

    return info


app = Flask(__name__)

# http://flask.pocoo.org/docs/0.12/config/#config
# By default Flask will serialize JSON objects in a way that the keys are ordered. This is done in order to
# ensure that independent of the hash seed of the dictionary the return value will be consistent to not trash external
# HTTP caches. You can override the default behavior by changing this variable. This is not recommended but might give
# you a performance improvement on the cost of cacheability.
app.config["JSON_SORT_KEYS"] = False

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string(
        """\
<html>
    <head>
        <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
        <title>get_upload_image_info</title>

        <script type="text/javascript" src="{{ url_for('static', filename='js/jquery-3.1.1.min.js') }}"></script>
        
        <style>
            /* 
                https://stackoverflow.com/a/7220510/5909792
                FOR function syntaxHighlight
            */
            pre {outline: 1px solid #ccc; padding: 5px; margin: 5px; white-space:pre-wrap; }
            .string { color: green; }
            .number { color: darkorange; }
            .boolean { color: blue; }
            .null { color: magenta; }
            .key { color: red; }
        
        </style>
        
    </head>
    <body>
        <p>get_upload_image_info:</p>
        <table>
            <tr>
                <td>
                    <form class="form__upload_file" action="/get_info_from_file" method="post" enctype="multipart/form-data">
                        <label>Image file: <input type="file" name="file" accept="image/*"></label>
                        <p><input type="submit"></p>
                    </form>
                </td>
                <td><div style="width: 100px;"></div></td>
                <td>
                    <form class="form__upload_url" action="/get_info_from_url" method="post" enctype="multipart/form-data">
                        <label>Image url: <input type="url" name="url" onkeydown="this.style.width = ((this.value.length + 1) * 8) + 'px';"></label>
                        <p><input type="submit"></p>
                    </form>
                </td>
            </tr>
        <table>

        <div class="block progress" style="display: none">
            <p>Пожалуйста, подождите, файл загружаются.</p>
            <progress class="progress upload" max="100" value="0"></progress>
        </div>

        <div class="result json show" style="display: none">
            <p>Результат от сервера:</p>
            <img width="200px" height="200px" alt="image"/><br/><br/>
            <pre></pre>
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

            // https://stackoverflow.com/a/7220510/5909792
            function syntaxHighlight(json) {
                json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                    var cls = 'number';
                    if (/^"/.test(match)) {
                        if (/:$/.test(match)) {
                            cls = 'key';
                        } else {
                            cls = 'string';
                        }
                    } else if (/true|false/.test(match)) {
                        cls = 'boolean';
                    } else if (/null/.test(match)) {
                        cls = 'null';
                    }
                    return '<span class="' + cls + '">' + match + '</span>';
                });
            }
        
            function on_success(data) {
                console.log(data);
                $('.block.progress').hide();
                    
                $('.result.json.show > img').attr('src', data.img_base64);
                
                if (data.img_base64.length > 100) {
                    data.img_base64 = data.img_base64.substring(0, 100) + "...";
                }
                
                var json_str = JSON.stringify(data, undefined, 4);
                console.log(json_str);
                
                json_str = syntaxHighlight(json_str);

                $('.result.json.show > pre').html(json_str);
                $('.result.json.show').show();
            }
        
            $(".form__upload_file").submit(function() {
                $('.block.progress').show();
                $('.result.json.show').hide();

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

                    success: on_success,
                });

                return false;
            });
            
            $(".form__upload_url").submit(function() {
                $('.block.progress').show();
                $('.result.json.show').hide();

                var thisForm = this;

                var url = $(this).attr("action");
                var method = $(this).attr("method");
                if (method === undefined) {
                    method = "get";
                }

                var data = $(this).serialize();
                                
                // For send file object:
                //// var input = $(".form__upload_file > input[type=file]");
                //// var data = new FormData(thisForm);

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
"""
    )


@app.route("/get_info_from_file", methods=["POST"])
def get_info_from_file():
    print(request.files)

    # check if the post request has the file part
    if "file" not in request.files:
        return redirect("/")

    file = request.files["file"]
    file_data = file.stream.read()

    info = get_image_info(file_data)
    info["img_base64"] = img_to_base64_html(file_data)

    return jsonify(info)


@app.route("/get_info_from_url", methods=["POST"])
def get_info_from_url():
    print(request.form)

    if "url" not in request.form:
        return redirect("/")

    url = request.form["url"]
    file_data = requests.get(url).content

    info = get_image_info(file_data)
    info["img_base64"] = img_to_base64_html(file_data)

    return jsonify(info)


if __name__ == "__main__":
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
