__author__ = 'ipetrash'


# TODO: сделать https://github.com/gil9red/DownloadByPornSite с гуем
# интерфейс позволяет серферить по тому сайту и простым нажатием на кнопку
# скачивать с сайта видео
#
# TODO: сделать интерфейс, который принимает ссылки на страницы с видео,
# добавляет их в список, а после показывает прогресс скачивания видео


from PySide.QtGui import *
from PySide.QtWebKit import QWebView
from PySide.QtCore import *


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.webView = QWebView()

        layout = QVBoxLayout()
        layout.addWidget(self.webView)
        self.setLayout(layout)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    w = Window()
    w.setWindowTitle("Пример 4")
    w.show()

    w.webView.load(QUrl("http://www.trahun.tv"))

    sys.exit(app.exec_())