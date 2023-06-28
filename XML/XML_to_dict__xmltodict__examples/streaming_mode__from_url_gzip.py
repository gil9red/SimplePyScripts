#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/martinblech/xmltodict#streaming-mode


import gzip
from urllib.request import urlopen

# pip install xmltodict
import xmltodict


# 241.8 MB
url = "http://discogs-data.s3-us-west-2.amazonaws.com/data/2018/discogs_20180201_artists.xml.gz"


def handle_artist(_, artist):
    print(artist["name"])
    return True


xmltodict.parse(
    gzip.open(urlopen(url)),
    item_depth=2,
    item_callback=handle_artist,
)
# The Persuader
# Mr. James Barth & A.D.
# Josh Wink
# Johannes Heil
# Heiko Laux
# ...
