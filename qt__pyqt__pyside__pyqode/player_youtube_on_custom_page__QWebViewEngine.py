#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView


if __name__ == "__main__":
    app = QApplication([])

    view = QWebEngineView()
    view.show()

    view.setHtml(
        """\
<html>
<body>
    <iframe width="560" height="315" src="https://www.youtube.com/embed/Cb-srOfRqNc" frameborder="0" allowfullscreen></iframe>
</body>
</html>
    """
    )

    app.exec()
