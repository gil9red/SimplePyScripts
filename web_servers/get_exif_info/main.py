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


from flask import Flask, jsonify
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    # Open image file for reading (binary mode)
    f = open('exif_this.jpg', mode='rb')

    categories_by_tag = get_exif_tags(f)
    return jsonify(categories_by_tag)


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
