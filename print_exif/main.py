#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64

# pip install exifread
import exifread


def get_exif_tags(file_object_or_file_name, as_category=True):
    if type(file_object_or_file_name) == str:
        # Open image file for reading (binary mode)
        file_object_or_file_name = open(file_object_or_file_name, mode="rb")

    # Return Exif tags
    tags = exifread.process_file(file_object_or_file_name)
    tags_by_value = dict()

    if not tags:
        print("Not tags")
        return tags_by_value

    print(f"Tags ({len(tags)}):")

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

        print(f'  "{tag}": {value}')

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

    print()

    return tags_by_value


if __name__ == "__main__":
    import json

    print("TAGS_BY_VALUE:")
    f = open("exif_this.jpg", mode="rb")
    tags_by_value = get_exif_tags(f, as_category=False)
    print(json.dumps(tags_by_value, sort_keys=True, ensure_ascii=False, indent=4))
    #
    # tags_by_value:
    # {
    #     "EXIF ExposureProgram": "Portrait Mode",
    #     "EXIF Padding": "[]",
    #     "Image Artist": "gil9red",
    #     "Image ExifOffset": "2202",
    #     "Image ImageDescription": "print_exif",
    #     "Image Make": "gil9red",
    #     "Image Padding": "[]",
    #     "Image XPAuthor": "gil9red",
    #     "Image XPComment": "https://github.com/gil9red/SimplePyScripts",
    #     "Image XPKeywords": "python;exif;example;питон",
    #     "Image XPSubject": "python, exif, example",
    #     "Image XPTitle": "print_exif"
    # }

    print("\n\n")
    print("CATEGORIES_BY_TAG:")
    f = open("exif_this.jpg", mode="rb")
    categories_by_tag = get_exif_tags(f)
    print(json.dumps(categories_by_tag, sort_keys=True, ensure_ascii=False, indent=4))
    #
    # categories_by_tag:
    # {
    #     "EXIF": {
    #         "ExposureProgram": "Portrait Mode",
    #         "Padding": "[]"
    #     },
    #     "Image": {
    #         "Artist": "gil9red",
    #         "ExifOffset": "2202",
    #         "ImageDescription": "print_exif",
    #         "Make": "gil9red",
    #         "Padding": "[]",
    #         "XPAuthor": "gil9red",
    #         "XPComment": "https://github.com/gil9red/SimplePyScripts",
    #         "XPKeywords": "python;exif;example;питон",
    #         "XPSubject": "python, exif, example",
    #         "XPTitle": "print_exif"
    #     }
    # }
