#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# TODO: лучше попробовать переписать на селениум, пример: https://github.com/gil9red/SimplePyScripts/blob/59322c5da8ce17ca5c68424b9db5fb82eda5e4dd/selenium__examples/screenshot.py

# TODO: сделать также PyQt5 вариант
# TODO: проверять поддерживаемые форматы по суффиксу file_name, если формат не поддерживается,
# кидать исключение с описание поддерживаемых параметров


from PyQt4.QtWebKit import QWebView, QWebPage
from PyQt4.QtGui import QApplication, QImage, QPainter
from PyQt4.QtCore import QEventLoop, QSize, QUrl
from PyQt4.QtNetwork import QNetworkProxyFactory


# Чтобы не было проблем запуска компов с прокси
QNetworkProxyFactory.setUseSystemConfiguration(True)


class WebPage(QWebPage):
    def userAgentForUrl(self, url) -> str:
        return (
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0"
        )


qApp = None


def url2image(url, file_name=None):
    """Function at the specified url downloads the page and stores it QImage object and returns it.
    If you pass file_name, then the function will save the picture in the file.

    Функция по указанному url загружает страницу и сохраняет ее объект QImage и возвращает его.
    Если передать file_name, тогда функция сохранит в файл картинку.
    """

    # Нужно создавать только один раз
    global qApp
    if qApp is None:
        qApp = QApplication([])

    # TODO: прятать вертикальный и горизонтальный ползунки
    # Загрузка url и ожидание ее
    view = QWebView()
    view.setPage(WebPage())

    view.load(QUrl(url))
    loop = QEventLoop()
    view.loadFinished.connect(loop.quit)
    loop.exec_()

    # Запрашиваем через javascript размеры страницы сайта
    width = (
        view.page().mainFrame().evaluateJavaScript("window.document.body.scrollWidth")
    )
    height = (
        view.page().mainFrame().evaluateJavaScript("window.document.body.scrollHeight")
    )

    # Устанавливаем границы документа
    view.page().setViewportSize(QSize(width, height))

    img = QImage(width, height, QImage.Format_ARGB32)
    painter = QPainter(img)
    painter.setRenderHint(QPainter.HighQualityAntialiasing)
    view.page().mainFrame().render(painter)
    painter.end()

    if file_name:
        img.save(file_name)

    return img


if __name__ == "__main__":
    img = url2image("https://www.google.ru/search?q=google+qwidget")
    img.save("html.png")
    # # Or:
    # img = url2image('https://www.google.ru/search?q=google+qwidget', "html.png")

    url2image("https://www.google.ru/search?q=cats&tbm=isch", "cats.png")

    # TODO: слишком большая высота получилась, нужно разобраться
    url2image("https://en.wikipedia.org/wiki/Python_(programming_language)", "wiki.jpg")
