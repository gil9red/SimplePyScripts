__author__ = 'ipetrash'


# Простой пример использования модуля PySide


from PySide.QtGui import *
# from PySide.QtCore import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    def says():
        print("Hello, Python!")

    label = QLabel("Hello, <b>PySize</b>!")

    button = QPushButton("Click me")
    button.clicked.connect(says)

    checkBox = QCheckBox("Показывать другое окно?")
    window_2 = QCalendarWidget()
    checkBox.stateChanged.connect(window_2.setVisible)

    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(button)
    layout.addWidget(checkBox)

    window = QWidget()
    window.setWindowTitle("Пример")
    window.setLayout(layout)
    window.show()

    sys.exit(app.exec_())