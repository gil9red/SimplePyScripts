#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Summary durations all video.

"""


import sys

from bs4 import BeautifulSoup

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *


QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

url_video_by_time_dict = dict()


def get_total_seconds(time_str):
    """
    Return seconds from strings: "hh:mm:ss", "mm:ss" and "ss".

    """

    total_seconds = 0

    time_part = list(map(int, time_str.split(":")))
    time_part_number = len(time_part)

    if time_part_number == 1:
        total_seconds += time_part[0]

    elif time_part_number == 2:
        total_seconds += time_part[0] * 60 + time_part[1]

    elif time_part_number == 3:
        total_seconds += time_part[0] * 3600 + time_part[1] * 60 + time_part[2]

    return total_seconds


def load_finished_handler(ok):
    if not ok:
        return

    doc = view.page().mainFrame().documentElement()

    def update_url_video_by_time_dict():
        global url_video_by_time_dict

        html = doc.toOuterXml()
        root = BeautifulSoup(html, "lxml")

        for item in root.select(".channels-content-item"):
            url = item.select_one(".yt-uix-tile-link")["href"]
            time_str = item.select_one(".video-time").text

            url_video_by_time_dict[url] = time_str

    # Fill dict
    update_url_video_by_time_dict()

    # Every 5 seconds
    timer = QTimer()
    timer.setInterval(5000)

    def timeout_handler():
        doc = view.page().mainFrame().documentElement()
        button = doc.findFirst(".load-more-button")

        # If button "More" visible
        is_load_more = not button.isNull()
        if is_load_more:
            # Fill dict
            update_url_video_by_time_dict()

        else:
            timer.stop()
            return

        # Click on button "More"
        print("More")
        button.evaluateJavaScript("this.click()")

    timer.timeout.connect(timeout_handler)
    timer.start()

    # Wait loading all video
    while timer.isActive():
        QApplication.instance().processEvents()

    print()
    print("Total:")
    print("  Videos: {}".format(len(url_video_by_time_dict)))
    print("  Durations: {}".format(list(url_video_by_time_dict.values())))

    # Summary duration
    sum_seconds = 0

    for time_str in url_video_by_time_dict.values():
        sum_seconds += get_total_seconds(time_str)

    mm, ss = divmod(sum_seconds, 60)
    hh, mm = divmod(mm, 60)
    sum_time_str = "%d:%02d:%02d" % (hh, mm, ss)

    print("  Summary duration (secs): {}".format(sum_seconds))
    print("  Summary duration: {}".format(sum_time_str))

    sys.exit()


if __name__ == "__main__":
    app = QApplication([])

    view = QWebView()
    # view.show()

    view.loadFinished.connect(load_finished_handler)

    url = QUrl("https://www.youtube.com/channel/UCWvMAvbk23gFzZ3BRUfACRA/videos")
    view.load(url)

    app.exec()
