#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *

except:
    try:
        from PyQt4.QtGui import *

    except:
        try:
            from PySide.QtGui import *
        except:
            pass


def get_img_urls():
    rs = requests.get("https://api.vk.com/method/photos.search?v=5.64")
    img_urls = rs.json()["response"]["items"]
    return [url["photo_130"] for url in img_urls]


if __name__ == "__main__":
    app = QApplication([])

    mw = QScrollArea()
    mw.setWindowTitle(__file__)
    mw.show()

    img_urls = get_img_urls()

    layout = QGridLayout()

    columns = 4
    i, j = 0, 0

    mw.setWindowTitle("Loading...")

    print("Images:", len(img_urls))

    url_by_label = dict()

    # Append labels on form
    for n, url in enumerate(img_urls):
        label = QLabel()
        label.setFixedSize(130, 130)
        label.setFrameStyle(QFrame.Box)
        layout.addWidget(label, i, j)

        url_by_label[url] = label

        j += 1
        if j >= columns:
            i += 1
            j = 0

    w = QWidget()
    w.setLayout(layout)
    mw.setWidget(w)

    for n, (url, label) in enumerate(url_by_label.items()):
        rs = requests.get(url)

        image = QImage.fromData(rs.content)
        pixmap = QPixmap.fromImage(image)

        label.setPixmap(pixmap)

        mw.setWindowTitle(f"{n}/{len(url_by_label)} Loading...")
        QApplication.processEvents()

    mw.setWindowTitle("Ok!")

    app.exec()
