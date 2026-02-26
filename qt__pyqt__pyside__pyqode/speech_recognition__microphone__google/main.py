#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://pythono.ru/speech-recognition-python/
# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/879912c8236a27a817c0284a51c9f61a034b407c/speech_recognition/microphone__google.py


import sys
import traceback


# pip install pyaudio
# pip install SpeechRecognition
import speech_recognition as sr

from PyQt5 import Qt


def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class SpeechRecognitionThread(Qt.QThread):
    about_text = Qt.pyqtSignal(str)

    language = "en-US"

    def run(self) -> None:
        try:
            r = sr.Recognizer()

            self.about_text.emit("Скажите что-нибудь...")

            with sr.Microphone() as source:
                audio = r.listen(source)

            self.about_text.emit("Анализирую речь...")

            text = r.recognize_google(audio, language=self.language)

            self.about_text.emit(f'Фраза: "{text}"')

        except sr.UnknownValueError:
            self.about_text.emit("Робот не расслышал фразу")

        except sr.RequestError as e:
            self.about_text.emit(f"Ошибка сервиса: {e}")

        except Exception as e:
            self.about_text.emit(f"Ошибка: {e}")

        finally:
            self.about_text.emit("")


class Window(Qt.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("speech_recognition__microphone__google")

        self.pb_microphone = Qt.QPushButton("🎤 SPEAK")
        self.pb_microphone.setFont(Qt.QFont("Arial", 16))

        self.cb_lang = Qt.QComboBox()
        self.cb_lang.addItems(["en-US", "ru-RU"])
        self.cb_lang.setCurrentIndex(1)

        self.pte_result = Qt.QPlainTextEdit()
        self.pte_result.setFont(Qt.QFont("Arial", 12))
        self.pte_result.setReadOnly(True)

        self.progress_bar = Qt.QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        self.progress_bar.setRange(0, 0)  # Infinity

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.pb_microphone)
        layout.addWidget(self.cb_lang)
        layout.addWidget(self.pte_result)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.thread = SpeechRecognitionThread()
        self.thread.about_text.connect(self.pte_result.appendPlainText)
        self.thread.started.connect(self.progress_bar.show)
        self.thread.finished.connect(self._speech_recognition_finish)

        # Start speech recognition
        self.pb_microphone.clicked.connect(self._speech_recognition_start)

    def _speech_recognition_start(self) -> None:
        self.pb_microphone.setEnabled(False)
        self.pte_result.clear()

        self.thread.language = self.cb_lang.currentText()
        self.thread.start()

    def _speech_recognition_finish(self) -> None:
        self.pb_microphone.setEnabled(True)
        self.progress_bar.hide()


if __name__ == "__main__":
    app = Qt.QApplication([])

    w = Window()
    w.show()
    w.resize(500, 500)

    app.exec()
