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

        # print('  "{}": {}'.format(tag, value))

        if not as_category:
            tags_by_value[tag] = value

        else:
            # Fill categories_by_tag
            if ' ' in tag:
                category, sub_tag = tag.split(' ', maxsplit=1)

                if category not in tags_by_value:
                    tags_by_value[category] = dict()

                tags_by_value[category][sub_tag] = value

            else:
                tags_by_value[tag] = value

    # print()

    return tags_by_value


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/master/human_byte_size.py
def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')


def get_image_info(file_name__or__bytes__or__bytes_io, pretty_json_str=False):
    data = file_name__or__bytes__or__bytes_io
    type_data = type(data)

    # File name
    if type_data == str:
        with open(data, mode='rb') as f:
            data = f.read()

    if type(data) == bytes:
        import io
        data = io.BytesIO(data)

    length = len(data.getvalue())
    exif = get_exif_tags(data)

    from PIL import Image
    img = Image.open(data)

    # TODO: append channels number (maybe img.mode parsing?)

    # Save order
    from collections import OrderedDict
    info = OrderedDict()
    info['length'] = OrderedDict()
    info['length']['value'] = length
    info['length']['text'] = sizeof_fmt(length)

    info['mode'] = img.mode
    info['format'] = img.format

    info['size'] = OrderedDict()
    info['size']['width'] = img.width
    info['size']['height'] = img.height

    info['exif'] = exif

    if pretty_json_str:
        import json
        info = json.dumps(info, indent=4, ensure_ascii=False)

    return info


if __name__ == '__main__':
    file_name = 'exif_this.jpg'

    data = open(file_name, 'rb').read()

    import io
    data_io = io.BytesIO(data)

    info_1 = get_image_info(file_name)
    info_2 = get_image_info(data)
    info_3 = get_image_info(data_io)
    assert info_1 == info_2 == info_3

    print(info_3)

    info_3 = get_image_info(data, pretty_json_str=True)
    print(info_3)
