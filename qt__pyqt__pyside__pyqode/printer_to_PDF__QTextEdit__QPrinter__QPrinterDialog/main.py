#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


# https://stackoverflow.com/a/8499716/5909792
html = """
<p>Red dot:</p><br>
<img width="100" src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />
"""


if __name__ == "__main__":
    app = Qt.QApplication([])

    printer = Qt.QPrinter()

    te = Qt.QTextEdit()
    te.setHtml(html)
    te.show()

    printer.setOutputFileName("result.pdf")
    te.print(printer)

    app.exec()
