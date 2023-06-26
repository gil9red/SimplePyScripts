#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt5.QtCore import QUrl, QEventLoop
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

# pip install PyQtWebEngine
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit()


sys.excepthook = log_uncaught_exceptions


# TODO: MainWindow

# TODO: Попробовать: https://github.com/WorldWideTelescope/pywwt/blob/99a3250afb325378d054ecb2045ef65b6ef073a6/pywwt/qt.py#L70
# TODO: попробовать
# def wait(until: callable, timeout=5000):
#     """Process events until condition is satisfied
#     Parameters
#     ----------
#     until: callable
#         Returns True when condition is satisfied.
#     timeout: int
#         Milliseconds to wait until TimeoutError is raised.
#     """
#     started = time.clock()
#     while not until():
#         qApp.processEvents(QEventLoop.ExcludeUserInputEvents)
#         if (time.clock() - started) * 1000 > timeout:
#             raise TimeoutError()


# pattern_text = """\
# Добрый день!
#
# Сегодня, {date} в {time}, я стал свидетелем нарушения правил стоянки транспортного средства. Водитель автомобиля {auto_number} припарковал его в зоне тротуара по адресу {adress}.
#
# Прошу Вас установить водителя данного транспортного средства и привлечь его к административной ответственности. Фотографии нарушителя прилагаю.
# """

TEXT_PATTERN = """\
Добрый день!

Сегодня, 20/08/2018 в 18:42, я стал свидетелем нарушения правил стоянки транспортного средства. Водитель
автомобиля Х322АТ 999 припарковал его в зоне тротуара по адресу г. Москва, пр. К. Маркса, д. 77/1.

Прошу Вас установить водителя данного транспортного средства и привлечь его к административной ответственности. Фотографии нарушителя прилагаю.
"""


def run_js_code(page: QWebEnginePage, code: str) -> object:
    loop = QEventLoop()

    result_value = {"value": None}

    def _on_callback(result: object):
        result_value["value"] = result

        loop.quit()

    page.runJavaScript(code, _on_callback)

    loop.exec()

    return result_value["value"]


class MyWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(
        self,
        level: "JavaScriptConsoleMessage",
        message: str,
        line_number: int,
        source_id: str,
    ):
        print(
            f"javascript_console_message: {level}, {message}, {line_number}, {source_id}",
            file=sys.stderr,
        )


with open("js/jquery-3.1.1.min.js") as f:
    jquery_text = f.read()
    jquery_text += "\nvar qt = { 'jQuery': jQuery.noConflict(true) };"


app = QApplication([])


# view.show()

# def _on_url_changed(url: QUrl):
#     mw.setWindowTitle(str(url))


url = "https://гибдд.рф/request_main"

page = MyWebEnginePage()
page.load(QUrl(url))

view = QWebEngineView()
view.setPage(page)

# page.urlChanged.connect(_on_url_changed)


def _on_load_finished(ok: bool):
    print(page.url().toString())

    page.runJavaScript(jquery_text)

    result = run_js_code(page, "document.title")
    print("run_java_script:", result)

    # TODO: обернуть в функцию has с css-selector
    result = run_js_code(page, "qt.jQuery('#surname_check').length > 0")
    print("run_java_script:", result)

    # Клик на флажок "С информацией ознакомлен"
    run_js_code(page, """qt.jQuery('input[name="agree"]').click();""")

    # Клик на кнопку "Подать обращение"
    run_js_code(page, """qt.jQuery('button.u-form__sbt').click();""")

    run_js_code(page, """qt.jQuery('#surname_check').val('SURNAME');""")
    run_js_code(page, """qt.jQuery('#firstname_check').val('FIRSTNAME');""")
    run_js_code(page, """qt.jQuery('input[name=patronymic]').val('PATRONYMIC');""")

    run_js_code(page, """qt.jQuery('#email_check').val('FOOBAR@EMAIL.COM');""")

    run_js_code(
        page,
        f"qt.jQuery('#message_check > textarea').val({TEXT_PATTERN!r});",
    )

    # code = """
    # console.log('testetst');
    #
    # // Клик на флажок "С информацией ознакомлен"
    # qt.jQuery('input[name="agree"]').click();
    #
    # // Клик на кнопку "Подать обращение"
    # qt.jQuery('button.u-form__sbt').click();
    # """
    #
    # result = run_js_code(page, code)
    # print('run_java_script:', result)

    # page.runJavaScript(code, lambda x: print('runJavaScript:', x))
    # page.runJavaScript("document.title", lambda x: print('runJavaScript:', x))

    print()


view.loadProgress.connect(
    lambda value: mw.setWindowTitle(f"{view.url().toString()} ({value}%)")
)
view.loadFinished.connect(_on_load_finished)

mw = QMainWindow()
mw.setCentralWidget(view)
mw.resize(800, 800)
mw.show()

app.exec()
