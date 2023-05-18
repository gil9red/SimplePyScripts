#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.request import urlopen
from lxml import etree


def get_video_url_from_24video_xxx(url):
    # url выглядят так: http://www.24video.xxx/video/view/2249418
    video_id = url.split("/")[-1]
    xml_info_url = f"http://www.24video.xxx/video/xml/{video_id}?mode=play"

    with urlopen(xml_info_url) as rs:
        root = etree.XML(rs.read())
        match = root.xpath("//video/@url")
        if match:
            return match[0]


if __name__ == "__main__":
    url = "http://www.24video.xxx/video/view/2249418"
    print(get_video_url_from_24video_xxx(url))

    url = "http://www.24video.xxx/video/view/1724382"
    print(get_video_url_from_24video_xxx(url))
