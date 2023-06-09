#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/7c3e004f8038cf7942226283fe0f5c184008b561/xor_crypto.py
def crypto_xor_1(message, secret):
    return "".join(chr(ord(c) ^ secret) for c in message)


class Window(Qt.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("crypto / decrypto")

        self.pte_text = Qt.QPlainTextEdit("Test / Тест")

        self.sb_key = Qt.QSpinBox()
        self.sb_key.setRange(1, 1000000)
        self.sb_key.setValue(42)
        self.sb_key.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Preferred)

        self.pb_convert = Qt.QPushButton("Convert")
        self.pb_convert.clicked.connect(self._on_convert)

        layout_command = Qt.QHBoxLayout()
        layout_command.addWidget(Qt.QLabel("Key:"))
        layout_command.addWidget(self.sb_key)

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.pte_text)
        layout.addLayout(layout_command)
        layout.addWidget(self.pb_convert)

        self.setLayout(layout)

    def _on_convert(self):
        text = self.pte_text.toPlainText()
        key = self.sb_key.value()

        text = crypto_xor_1(text, key)

        self.pte_text.setPlainText(text)


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = Window()
    mw.show()

    app.exec()
