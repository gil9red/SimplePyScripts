#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


url = 'https://www.youtube.com/playlist?list=PLqf5JRBicHXnV4fUNPJtE2YFAjPMHRX4K'
# url = 'https://www.youtube.com/playlist?list=PLKom48yw6lJpyYN2Q_zmss68ntjzxxpHd'

import grab

g = grab.Grab()
g.go(url)

# match_list = g.doc.select('//*[@class="pl-video yt-uix-tile "]')
# for i, item in enumerate(match_list, 1):
#     # TODO: Не самый удачный вариант, лучше от текущего элемента искать, или создать два запроса xpath --
#     # для списка видео и для списка продолжительности видео и соединить их
#     print(i, item.attr('data-title'), item.select('(//*[@class="timestamp"])[{}]'.format(i)).text())

video_list = g.doc.select('//*[@class="pl-video yt-uix-tile "]')
time_list = g.doc.select('//*[@class="timestamp"]')

total_seconds = 0

print('Playlist:')
for i, (video, time) in enumerate(zip(video_list, time_list), 1):
    time_str = time.text()
    print('{}. {} ({})'.format(i, video.attr('data-title'), time_str))

    time_split = time_str.split(':')
    if len(time_split) == 3:
        h, m, s = map(int, time_split)
        total_seconds += h * 60 * 60 + m * 60 + s
    elif len(time_split) == 2:
        m, s = map(int, time_split)
        total_seconds += m * 60 + s
    else:
        total_seconds += int(time_split[0])

# h, m, s = total_seconds // 3600, total_seconds // 60 % 60, total_seconds % 60
# print('\nTotal time: {}:{}:{} ({} total seconds).'.format(h, m, s, total_seconds))

from datetime import timedelta
print('\nTotal time: {} ({} total seconds).'.format(timedelta(seconds=total_seconds), total_seconds))
