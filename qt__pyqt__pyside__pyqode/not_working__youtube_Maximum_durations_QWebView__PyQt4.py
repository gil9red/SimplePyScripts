#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Maximum durations.

"""


import sys

from bs4 import BeautifulSoup

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *


QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

video_time_list = set()
video_link_list = set()


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


def load_finished_handler(ok) -> None:
    if not ok:
        return

    doc = view.page().mainFrame().documentElement()

    def get_video_time_list():
        html = doc.toOuterXml()
        root = BeautifulSoup(html, "lxml")

        return [title.text for title in root.select(".video-time")]

    def get_video_link_list():
        html = doc.toOuterXml()
        root = BeautifulSoup(html, "lxml")

        return {a["href"] for a in root.select(".yt-uix-tile-link")}

    # Get video time and append to list
    global video_time_list
    video_time_list.update(get_video_time_list())

    # Get video link and append to list
    global video_link_list
    video_link_list.update(get_video_link_list())

    # Every 5 seconds
    timer = QTimer()
    timer.setInterval(5000)

    def timeout_handler() -> None:
        doc = view.page().mainFrame().documentElement()
        button = doc.findFirst(".load-more-button")

        # If button "More" visible
        is_load_more = not button.isNull()
        if is_load_more:
            # Get video time and append global list
            global video_time_list
            video_time_list.update(get_video_time_list())

            # Get video link and append to list
            global video_link_list
            video_link_list.update(get_video_link_list())

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
    print(f"  Videos: {len(video_link_list)}, {video_link_list}")
    print(f"  Durations: {len(video_time_list)}, {video_time_list}")

    # Find maximum duration
    max_total_seconds = 0
    max_time_str = None

    for time_str in video_time_list:
        total_seconds = get_total_seconds(time_str)
        if total_seconds > max_total_seconds:
            max_total_seconds = total_seconds
            max_time_str = time_str

    print(f"  Max durations: {max_time_str}")

    sys.exit()


if __name__ == "__main__":
    app = QApplication([])

    view = QWebView()
    # view.show()

    view.loadFinished.connect(load_finished_handler)

    url = QUrl("https://www.youtube.com/channel/UCWvMAvbk23gFzZ3BRUfACRA/videos")
    view.load(url)

    app.exec()
