__author__ = 'ipetrash'


"""Пример таймера."""


from PySide.QtCore import *
import sys


def say():
    print("say!")


app = QCoreApplication(sys.argv)

t = QTimer()
t.setInterval(1000)
t.timeout.connect(say)
t.start()

sys.exit(app.exec_())