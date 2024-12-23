#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from api.common import Video


url = "https://www.youtube.com/watch?v=rgYQ7nUulAQ"
video_id = Video.get_id_from_url(url)
assert video_id == "rgYQ7nUulAQ"

new_url = Video.get_url(video_id)
assert url == new_url

video = Video.get_from(url)
print(video)
# Video(id='rgYQ7nUulAQ', url='https://www.youtube.com/watch?v=rgYQ7nUulAQ', title='Building a Website (P1D2) - Live Coding with Jesse', duration_seconds=1929, duration_text='00:32:09', seq=None, is_live_now=False, view_count=24602, create_date=datetime.date(2017, 5, 3), create_date_raw='Прямой эфир состоялся 3 мая 2017 г.', is_lasy=False)

assert video.create_date
