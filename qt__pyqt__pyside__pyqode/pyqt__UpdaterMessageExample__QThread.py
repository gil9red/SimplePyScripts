#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.Qt import (
    QThread, pyqtSignal, QMessageBox, QApplication, QWidget, QLabel,
    QPlainTextEdit, QVBoxLayout, QProgressDialog
)


class AboutUpdateThread(QThread):
    about_update = pyqtSignal(str)

    def run(self):
        while True:
            # Делаем какие-то действия и проверки, и вызываем сигнал about_update,
            # чтобы сообщить о новой версии
            # ...
            # if ...:

            self.about_update.emit('Доступна новая версия 2.1.1')

            # 6 hours
            QThread.sleep(6 * 60 * 60)


class RunFuncThread(QThread):
    run_finished = pyqtSignal(object)

    def __init__(self, func):
        super().__init__()

        self.func = func

    def run(self):
        self.run_finished.emit(self.func())


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.log = QPlainTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Log:'))
        layout.addWidget(self.log)

        self.setLayout(layout)

        self.thread = AboutUpdateThread(self)
        self.thread.about_update.connect(self.on_about_update)
        self.thread.start()

    def add_log(self, text):
        self.log.appendPlainText(text)

    def on_about_update(self, text):
        self.add_log("Пришло обновление '{}'".format(text))

        mb = QMessageBox()
        mb.setWindowTitle("Доступно обновление")
        mb.setText("Сейчас доступно обновление")
        mb.setDetailedText(text)
        mb.addButton("Обновить", QMessageBox.AcceptRole)
        mb.addButton("Отклонить", QMessageBox.RejectRole)

        if mb.exec() == QMessageBox.RejectRole:
            self.add_log('Пользователь отказался от обновления...')
            return

        self.add_log('Выполняю обновление...')

        # ...
        # Обновляемся
        progress_dialog = QProgressDialog(self)

        def foo():
            # Для эмитации работы делаем задержку на 2 секунды
            import time
            time.sleep(2)

        thread = RunFuncThread(func=foo)
        thread.run_finished.connect(progress_dialog.close)
        thread.start()

        progress_dialog.setWindowTitle('Please wait...')
        progress_dialog.setLabelText(progress_dialog.windowTitle())
        progress_dialog.setRange(0, 0)
        progress_dialog.exec()
        # ...

        self.add_log('Обновление поставлено успешно...')


if __name__ == '__main__':
    app = QApplication([])

    mw = Window()
    mw.resize(400, 400)
    mw.show()

    app.exec()
