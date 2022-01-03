#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os.path
from pathlib import Path


profile_name = 'ef941a74.dev-edition-default'

# Example: C:\Users\<user>\AppData\Roaming\Mozilla\Firefox\Profiles\<profile>\places.sqlite
dir_profiles = Path(os.path.expandvars(r'%AppData%\Mozilla\Firefox\Profiles'))
dir_profile = dir_profiles / profile_name

file_name_places = dir_profile / 'places.sqlite'
file_name_session = dir_profile / 'sessionstore.jsonlz4'
