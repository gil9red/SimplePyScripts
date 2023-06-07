__author__ = "ipetrash"


# Пример показывает как можно создать простое окно с небольшим функционалом,
# наследуюсь от класса QWidget


from PySide import QtGui


class SimpleWindow(QtGui.QWidget):
    """Просто окно"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Простое окно")

        self.lw_log = QtGui.QListWidget()
        self.le_mess = QtGui.QLineEdit()
        self.pb_send = QtGui.QPushButton("Отправить")
        self.pb_send.clicked.connect(self.slot_add_log)

        layout_cmd = QtGui.QHBoxLayout()
        layout_cmd.addWidget(self.le_mess)
        layout_cmd.addWidget(self.pb_send)

        layout_main = QtGui.QVBoxLayout()
        layout_main.addWidget(self.lw_log)
        layout_main.addLayout(layout_cmd)

        self.setLayout(layout_main)

    def slot_add_log(self):
        text = self.le_mess.text()
        if text:
            self.lw_log.addItem(text)


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)

    w = SimpleWindow()
    w.show()

    sys.exit(app.exec_())
