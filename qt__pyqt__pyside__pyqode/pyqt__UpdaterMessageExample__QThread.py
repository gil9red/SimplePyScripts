#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import (
    QThread,
    pyqtSignal,
    QMessageBox,
    QApplication,
    QWidget,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
)


class AboutUpdateThread(QThread):
    about_update = pyqtSignal(str)

    def run(self) -> None:
        while True:
            # Делаем какие-то действия и проверки, и вызываем сигнал about_update,
            # чтобы сообщить о новой версии
            # ...
            # if ...:

            self.about_update.emit("Доступна новая версия 2.1.1")

            # 6 hours
            QThread.sleep(6 * 60 * 60)


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.log = QPlainTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log)

        self.setLayout(layout)

        self.thread = AboutUpdateThread(self)
        self.thread.about_update.connect(self.on_about_update)
        self.thread.start()

    def add_log(self, text) -> None:
        self.log.appendPlainText(text)

    def on_about_update(self, text) -> None:
        self.add_log(f"Пришло обновление '{text}'")

        mb = QMessageBox()
        mb.setWindowTitle("Доступно обновление")
        mb.setText("Сейчас доступно обновление")
        mb.setDetailedText(text)
        button_ok = mb.addButton("Обновить", QMessageBox.AcceptRole)
        button_cancel = mb.addButton("Отклонить", QMessageBox.RejectRole)

        mb.exec()

        if mb.clickedButton() == button_cancel:
            self.add_log("Пользователь отказался от обновления...")
            return

        self.add_log("Выполняю обновление...")

        # ...
        # Обновляемся
        # ...

        self.add_log("Обновление поставлено успешно...")


if __name__ == "__main__":
    app = QApplication([])

    mw = Window()
    mw.resize(400, 400)
    mw.show()

    app.exec()
