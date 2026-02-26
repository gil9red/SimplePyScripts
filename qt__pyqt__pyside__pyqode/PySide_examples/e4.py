__author__ = "ipetrash"


import time
from threading import Thread

from grab import Grab
from PySide.QtGui import *


def get_confucius_quotes():
    g = Grab()
    # http://ru.wikiquote.org/wiki/Конфуций
    url = (
        "http://ru.wikiquote.org/wiki/%D0%9A%D0%BE%D0%BD%D1%84%D1%83%D1%86%D0%B8%D0%B9"
    )
    g.go(url)

    quotes = list()
    for el in g.doc.select("//h2/following-sibling::ul/li"):
        quotes.append(el.text())

    return quotes


class MyThread(Thread):
    def __init__(self, log) -> None:
        super().__init__()
        self.log = log

    def run(self) -> None:
        for i, quote in enumerate(get_confucius_quotes(), 1):
            self.log.append(f'{i}. "{quote}"\n')
            time.sleep(0.1)  # задержка каждые 100 миллисекунд


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.te_quotes = QTextEdit()
        self.te_quotes.setReadOnly(True)
        self.setCentralWidget(self.te_quotes)

    def slot_refresh(self) -> None:
        self.te_quotes.clear()
        thread = MyThread(self.te_quotes)
        thread.start()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    w = Window()
    w.setWindowTitle("Пример 4")
    w.show()
    w.slot_refresh()

    sys.exit(app.exec_())
