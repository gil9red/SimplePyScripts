__author__ = "ipetrash"


"""Пример таймера."""


import sys
from PySide.QtCore import *


def say():
    print("say!")


app = QCoreApplication(sys.argv)

t = QTimer()
t.setInterval(1000)
t.timeout.connect(say)
t.start()

sys.exit(app.exec_())
