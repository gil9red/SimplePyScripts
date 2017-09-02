#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/master/print_exif/main.py
def get_exif_tags(file_object_or_file_name, as_category=True):
    if type(file_object_or_file_name) == str:
        # Open image file for reading (binary mode)
        file_object_or_file_name = open(file_object_or_file_name, mode='rb')

    # Return Exif tags
    # pip install exifread
    import exifread
    tags = exifread.process_file(file_object_or_file_name)
    tags_by_value = dict()

    if not tags:
        print('Not tags')
        return tags_by_value

    print('Tags ({}):'.format(len(tags)))

    for tag, value in tags.items():
        # Process value
        try:
            if value.field_type == 1:
                try:
                    # If last 2 items equals [0, 0]
                    if value.values[-2:] == [0, 0]:
                        value = bytes(value.values[:-2]).decode('utf-16')
                    else:
                        value = bytes(value.values).decode('utf-16')

                except:
                    value = str(value.values)
            else:
                value = value.printable

            value = value.strip()

        except:
            # Example tag JPEGThumbnail
            if type(value) == bytes:
                import base64
                value = base64.b64encode(value).decode()

        print('  "{}": {}'.format(tag, value))

        if not as_category:
            tags_by_value[tag] = value

        else:
            # Fill categories_by_tag
            if ' ' in tag:
                category, sub_tag = tag.split(' ')

                if category not in tags_by_value:
                    tags_by_value[category] = dict()

                tags_by_value[category][sub_tag] = value

            else:
                tags_by_value[tag] = value

    print()

    return tags_by_value


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

    import io
    bytes_io = io.BytesIO(img_bytes)

    from PIL import Image
    img = Image.open(bytes_io)

    import base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    # print(img_base64)

    return 'data:image/{};base64,'.format(img.format.lower()) + img_base64


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/master/human_byte_size.py
def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


from flask import Flask, jsonify, render_template_string, redirect, request
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template_string('''\
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
        <form class="form__upload_file" action="/get_info" method="post" enctype="multipart/form-data">
            <p>get_upload_image_info:</p>
            <p><input type="file" name="file" accept="image/*"></p>
            <p><input type="submit"></p>
        </form>

        <div class="block progress" style="display: none">
            <p>Пожалуйста, подождите, файл загружаются.</p>
            <progress class="progress upload" max="100" value="0"></progress>
        </div>

        <div class="result json show" style="display: none">
            <p>Результат от сервера:</p>
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

                    success: function(data) {
                        console.log(data);
                        $('.block.progress').hide();
                        
                        var json_str = JSON.stringify(data, undefined, 4);
                        console.log(json_str);
                        
                        json_str = syntaxHighlight(json_str);

                        $('.result.json.show > pre').html(json_str);
                        $('.result.json.show').show();
                    },
                });

                return false;
            });
        });
        </script>
    </body>
</html>
''')


@app.route("/get_info", methods=['POST'])
def get_info():
    print(request.files)

    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect('/')

    file = request.files['file']
    file_data = file.stream.read()
    length = len(file_data)

    img_base64 = img_to_base64_html(file_data)

    import io
    exif = get_exif_tags(io.BytesIO(file_data))

    from PIL import Image
    img = Image.open(io.BytesIO(file_data))

    return jsonify({
        'exif': exif,
        'img_base64': img_base64,
        'length': {
            'value': length,
            'text': sizeof_fmt(length),
        },
        'size': {
            'width': img.width,
            'height': img.height,
        },
    })


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
