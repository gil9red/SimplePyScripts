#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

# pip install pyqt5
from PyQt5 import Qt

# https://github.com/secdev/scapy
# pip install scapy
from scapy.all import sniff


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class SniffThread(Qt.QThread):
    about_new_data = Qt.pyqtSignal(str)

    def _packethandler(self, pkt):
        data = pkt.summary()
        print(data)

        self.about_new_data.emit(data)

    def run(self):
        sniff(filter="tcp", prn=self._packethandler)


class MainWindow(Qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sniff with scapy")

        self.lw_packet = Qt.QListWidget()

        self.cb_log = Qt.QCheckBox("Write log")
        self.cb_log.setChecked(True)

        self.pb_clear = Qt.QPushButton("Clear")
        self.pb_clear.clicked.connect(self.lw_packet.clear)

        self.cb_autoscroll = Qt.QCheckBox("Autoscroll")

        layout = Qt.QHBoxLayout()
        layout.addWidget(self.cb_log)
        layout.addWidget(self.cb_autoscroll)
        layout.addStretch()
        layout.addWidget(self.pb_clear)

        main_layout = Qt.QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.lw_packet)

        central_widget = Qt.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.thread = SniffThread()
        self.thread.about_new_data.connect(self._append_new_item)
        self.thread.start()

    def _append_new_item(self, data):
        # Если флаг не стоит
        if not self.cb_log.isChecked():
            return

        self.lw_packet.addItem(data)

        # Если нужно автоматически прокручивать список вниз
        if self.cb_autoscroll.isChecked():
            self.lw_packet.scrollToBottom()


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec_()
