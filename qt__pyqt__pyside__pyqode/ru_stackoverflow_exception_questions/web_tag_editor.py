#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys

from datetime import datetime
from urllib.parse import urljoin, quote

from PySide.QtCore import QEventLoop, QTimer
from PySide.QtWebKit import QWebPage, QWebView, QWebSettings
from PySide.QtNetwork import QNetworkProxyFactory


def get_logger(name, file="log.txt", encoding="utf8"):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s"
    )

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)
    return log


logger = get_logger("web_tag_editor")


class WebPage(QWebPage):
    def userAgentForUrl(self, url) -> str:
        return (
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
        )


# Чтобы не было проблем запуска компов с прокси:
QNetworkProxyFactory.setUseSystemConfiguration(True)

QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)


class WebTagEditor(QWebView):
    def __init__(self, login, password, question_url) -> None:
        super().__init__()

        self.login = login
        self.password = password
        self.question_url = question_url

        self.our_tag = "исключения"

        self.setWindowTitle("WebTagEditor")

        logger.debug(
            "WebTagEditor: login: %s, password: %s, question_url: %s",
            login,
            "*" * len(password),
            question_url,
        )

        self.setPage(WebPage())

    def go(self) -> None:
        self.load("https://ru.stackoverflow.com/users/login")
        self.doc.findFirst("#email").setAttribute("value", self.login)
        self.doc.findFirst("#password").setAttribute("value", self.password)
        self.doc.findFirst("#submit-button").evaluateJavaScript("this.click()")

        # После клика на submit-button ждем пока прогрузится страница
        loop = QEventLoop()
        self.loadFinished.connect(loop.quit)
        loop.exec_()

        self.load(self.question_url)

        # Проверим, что наш тег не списке тегов
        tags = self.all_tags()
        logger.debug("Все тэги: %s.", tags)

        if self.our_tag in tags:
            logger.debug('Наш тэг "%s" уже есть в списке тэгов.', self.our_tag)
            return

        # TODO: Минимальная длина заголовка 15 символов.
        # TODO: Отсутствует тело сообщения.
        # TODO: проверяка на то, что править можно

        # Кликаем на "править"
        href = self.doc.findFirst(".question .suggest-edit-post").attribute("href")
        href = urljoin(self.url().toString(), href)
        logger.debug("Ссылка на страницу редактирования вопроса: %s.", href)

        self.load(href)

        tags = self.all_tags()
        logger.debug("Все тэги: %s.", tags)

        # Уже было замечен баг (http://meta.ru.stackoverflow.com/questions/2736), когда количество тегов
        # на странице вопроса и в редакторе отличалось, поэтому добавим еще проверку
        if self.our_tag in tags:
            logger.debug('Наш тэг "%s" уже есть в списке тэгов.', self.our_tag)
            return

        # Добавление нашего тега
        self.add_tag(self.our_tag)

        tags = self.all_tags()
        logger.debug("Все тэги: %s.", tags)

        # Паранойя: проверяем, что добавление тэга прошло удачно
        if self.our_tag not in tags:
            logger.warn(
                'Нашего тэга "%s" нет в списке тэгов, так не должно быть.', self.our_tag
            )
            return

        # Добавление описания изменений
        logger.debug("Добавление описания изменений.")
        js = f'$("#edit-comment")[0].value = "Добавлена метка: {self.our_tag}.";'
        self.evaluate_java_script(js)

        quote_tags = "+".join([quote(tag) for tag in self.all_tags()])

        # TODO: не сработало
        # Имитация последствия ввода тега
        logger.debug("Имитация последствия ввода тега.")
        js = f"""
        $.ajax({{
        'type': 'GET',
        'url': 'api/tags/langdiv?tags={quote_tags}&_={int(datetime.now().timestamp() * 1000)}'
        }});
        """
        self.evaluate_java_script(js)

        # Ждем немного пока выполняется ajax-запрос
        loop = QEventLoop()
        QTimer.singleShot(3 * 1000, loop.quit)
        loop.exec_()

        logger.debug('Клик на кнопку "Сохранить изменения".')
        self.doc.findFirst("#submit-button").evaluateJavaScript("this.click()")

        # После клика на submit-button ждем пока прогрузится страница
        loop = QEventLoop()
        self.loadFinished.connect(loop.quit)
        loop.exec_()

    def load(self, url) -> None:
        logger.debug("Начата загрузка url: %s.", url)
        super().load(url)

        # Ждем пока прогрузится страница
        loop = QEventLoop()
        self.loadFinished.connect(loop.quit)
        loop.exec_()

        logger.debug("Загрузка url завершена.")

    @property
    def doc(self):
        return self.page().mainFrame().documentElement()

    def evaluate_java_script(self, js) -> None:
        logger.debug('Исполнение js-кода:\n"%s".', js)
        self.doc.evaluateJavaScript(js)
        # result = self.doc.evaluateJavaScript(js)
        # logger.debug('Результат:\n"%s".', str(result).encode())

    def add_tag(self, name) -> None:
        logger.debug('Добавление тэга: "%s".', name)

        js = f"""
        var script = '<span class="post-tag rendered-element">{name}<span class="delete-tag" title="удалить эту метку"></span></span>';
        $('.tag-editor > span').append(script);
        """
        self.evaluate_java_script(js)

    def all_tags(self):
        tag_elements = self.doc.findAll(".post-tag.rendered-element")
        if tag_elements.count():
            tags = [i.toPlainText() for i in tag_elements]
        else:
            tags = [i.toPlainText() for i in self.doc.findAll(".post-tag")]

        return list(set(tags))
