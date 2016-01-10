#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# url = 'https://www.youtube.com/playlist?list=PLqf5JRBicHXnV4fUNPJtE2YFAjPMHRX4K'

import grab

g = grab.Grab(open('ut_pl.html').read())
# g.go(url)

# match_list = g.doc.select('//*[@class="pl-video yt-uix-tile "]')
# for i, item in enumerate(match_list, 1):
#     # TODO: Не самый удачный вариант, лучше от текущего элемента искать, или создать два запроса xpath --
#     # для списка видео и для списка продолжительности видео и соединить их
#     print(i, item.attr('data-title'), item.select('(//*[@class="timestamp"])[{}]'.format(i)).text())

video_list = g.doc.select('//*[@class="pl-video yt-uix-tile "]')
time_list = g.doc.select('//*[@class="timestamp"]')

for i, (video, time) in enumerate(zip(video_list, time_list), 1):
    print('{}. {} ({})'.format(i, video.attr('data-title'), time.text()))
