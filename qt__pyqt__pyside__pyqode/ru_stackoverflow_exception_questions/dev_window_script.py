#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime
from urllib.parse import quote

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *


# Чтобы не было проблем запуска компов с прокси:
QNetworkProxyFactory.setUseSystemConfiguration(True)

QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)


class WebPage(QWebPage):
    def userAgentForUrl(self, url):
        return (
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
        )


self.view = QWebView()
self.view.setPage(WebPage())
self.setCentralWidget(self.view)

self.view.show()

self.view.load("https://ru.stackoverflow.com/users/login")

# Ждем пока прогрузится страница
loop = QEventLoop()
self.view.loadFinished.connect(loop.quit)
loop.exec_()

self.doc = self.view.page().mainFrame().documentElement()
self.doc.findFirst("#email").setAttribute("value", "<email>")
self.doc.findFirst("#password").setAttribute("value", "<password>")
self.doc.findFirst("#submit-button").evaluateJavaScript("this.click()")

# Ждем пока прогрузится страница
loop = QEventLoop()
self.view.loadFinished.connect(loop.quit)
loop.exec_()


self.view.load("https://ru.stackoverflow.com/questions/8341")

# TODO: Минимальная длина заголовка 15 символов.
# TODO: Отсутствует тело сообщения.
# TODO: проверяка на то, что править можно
# TODO: проверка на отсутсвие тега
# TODO: удалять из базы измененный вопрос

# Ждем пока прогрузится страница
loop = QEventLoop()
self.view.loadFinished.connect(loop.quit)
loop.exec_()

self.doc = self.view.page().mainFrame().documentElement()

# Кликаем на "править"
href = self.doc.findFirst(".question .suggest-edit-post").attribute("href")
js = f'window.location.href = "{href}";'
print(href, js)
self.doc.evaluateJavaScript(js)

# Ждем пока прогрузится страница
loop = QEventLoop()
self.view.loadFinished.connect(loop.quit)
loop.exec_()

self.doc = self.view.page().mainFrame().documentElement()
# js = '$(".tag-editor input")[0].value = "{}";'.format("исключения")
# self.doc.evaluateJavaScript(js);


def add_tag(name, doc):
    js = f"""
    var script = '<span class="post-tag rendered-element">{name}<span class="delete-tag" title="удалить эту метку"></span></span>';
    $('.tag-editor > span').append(script);
    """
    print(js)
    doc.evaluateJavaScript(js)


add_tag("исключения", self.doc)


# Добавление описания метки
js = '$("#edit-comment")[0].value = "Добавлена метка: исключения";'
self.doc.evaluateJavaScript(js)

# TODO: при вводе тегов отправляет запрос вида. Без его вызова,
# я думаю, не получится сохранить изменения:
# https://ru.stackoverflow.com/api/tags/langdiv?tags=sqlserver+sql+k&_=1458326254816

# TODO: временный костыль
qu = quote("исключения")

tags = [i.toPlainText() for i in self.doc.findAll(".post-tag.rendered-element")]
tags = "+".join(tags)
tags = tags.replace("исключения", qu)
print(tags)

# Имитация последствия ввода тега
js = f"""
$.ajax({{
'type': 'GET',
'url': 'api/tags/langdiv?tags={tags}&_={int(datetime.now().timestamp() * 1000)}'
}});
"""
print(js)
print(self.doc.evaluateJavaScript(js))
