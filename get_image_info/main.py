#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


import json
import io
import sys

from pathlib import Path

from PIL import Image

sys.path.append(str(Path(__file__).resolve().parent.parent))
from human_byte_size import sizeof_fmt


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


def get_image_info(file_name__or__bytes__or__bytes_io, pretty_json_str=False):
    data = file_name__or__bytes__or__bytes_io
    type_data = type(data)

    # File name
    if type_data == str:
        with open(data, mode='rb') as f:
            data = f.read()

    if type(data) == bytes:
        data = io.BytesIO(data)

    length = len(data.getvalue())
    exif = get_exif_tags(data)

    img = Image.open(data)

    # Save order
    info = dict()
    info['length'] = {
        'value': length,
        'text': sizeof_fmt(length),
    }

    info['format'] = img.format
    info['mode'] = img.mode
    info['channels'] = len(img.getbands())
    info['bit_color'] = {
        '1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32,
        'CMYK': 32, 'YCbCr': 24, 'I': 32, 'F': 32
    }[img.mode]

    info['size'] = {
        'width': img.width,
        'height': img.height,
    }

    info['exif'] = exif

    if pretty_json_str:
        info = json.dumps(info, indent=4, ensure_ascii=False)

    return info


if __name__ == '__main__':
    file_name = 'exif_this.jpg'

    data = open(file_name, 'rb').read()
    data_io = io.BytesIO(data)

    info_1 = get_image_info(file_name)
    info_2 = get_image_info(data)
    info_3 = get_image_info(data_io)
    assert info_1 == info_2 == info_3

    print(info_3)

    info_3 = get_image_info(data, pretty_json_str=True)
    print(info_3)
