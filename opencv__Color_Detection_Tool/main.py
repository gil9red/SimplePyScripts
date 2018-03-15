#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://itnotesblog.ru/note.php?id=272#sthash.e5tCuHk0.dpbs


from PyQt5 import Qt
from mainwidget_ui import Ui_MainWidget
import cv2
import numpy as np


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, 'Error', text)
    quit()


import sys
sys.excepthook = log_uncaught_exceptions


CONFIG_FILE_NAME = "config.ini"


class MainWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        self.setWindowTitle('Color Detection Tool')

        self.ui.rbResult.setChecked(True)

        self.m_settings = Qt.QSettings(CONFIG_FILE_NAME, Qt.QSettings.IniFormat)
        self.m_lastLoadPath = "."
        self.m_mat = None

        for w in self.findChildren(Qt.QSlider):
            w.sliderMoved.connect(self.refresh_HSV)

            name = w.objectName()
            w.setValue(int(self.m_settings.value(name, w.value())))
            sp = self.findChild(Qt.QSpinBox, "sp" + name[2:])
            if sp:
                sp.setMinimum(w.minimum())
                sp.setMaximum(w.maximum())
                sp.setValue(w.value())
                sp.valueChanged.connect(self.refresh_HSV)

        for w in self.findChildren(Qt.QSpinBox):
            w.valueChanged.connect(self.refresh_HSV)

        for w in self.findChildren(Qt.QRadioButton):
            w.clicked.connect(self.refresh_HSV)

        self.ui.bnLoad.clicked.connect(self.on_load)

    def on_load(self):
        file_name = Qt.QFileDialog.getOpenFileName(self, "Load image", self.m_lastLoadPath, "Images (*.jpg *.jpeg *.png *.bmp)")[0]
        if not file_name:
            return

        self.m_lastLoadPath = Qt.QFileInfo(file_name).absolutePath()

        self.m_mat = cv2.imread(file_name)
        self.m_mat = cv2.cvtColor(self.m_mat, cv2.COLOR_BGR2RGB)

        self.refresh_HSV()
    
    @staticmethod
    def numpy_array_to_QImage(numpy_array):
        if len(numpy_array.shape) == 3:
            height, width, channel = numpy_array.shape
            bytes_per_line = 3 * width
            return Qt.QImage(numpy_array.data, width, height, bytes_per_line, Qt.QImage.Format_RGB888)
        else:
            height, width = numpy_array.shape
            bytes_per_line = 1 * width
            return Qt.QImage(numpy_array.data, width, height, bytes_per_line, Qt.QImage.Format_Indexed8)
    
    def refresh_HSV(self):
        if self.m_mat is None:
            return

        if self.ui.rbOriginal.isChecked():
            result_img = self.numpy_array_to_QImage(self.m_mat)

        else:
            hue_from = self.ui.slHueFrom.value()
            hue_to = max(hue_from, self.ui.slHueTo.value())

            saturation_from = self.ui.slSaturationFrom.value()
            saturation_to = max(saturation_from, self.ui.slSaturationTo.value())

            value_from = self.ui.slValueFrom.value()
            value_to = max(value_from, self.ui.slValueTo.value())

            thresholded_mat = cv2.cvtColor(self.m_mat, cv2.COLOR_RGB2HSV)
            print(np.array((hue_from, saturation_from, value_from), np.uint8))
            print(np.array((hue_to, saturation_to, value_to), np.uint8))
            # Отфильтровываем только то, что нужно, по диапазону цветов
            thresholded_mat = cv2.inRange(
                thresholded_mat,
                np.array((hue_from, saturation_from, value_from), np.uint8),
                np.array((hue_to, saturation_to, value_to), np.uint8)
            )

            # Убираем шум
            thresholded_mat = cv2.erode(
                thresholded_mat,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )
            thresholded_mat = cv2.dilate(
                thresholded_mat,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )

            # Замыкаем оставшиеся крупные объекты
            thresholded_mat = cv2.dilate(
                thresholded_mat,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )
            thresholded_mat = cv2.erode(
                thresholded_mat,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )

            if self.ui.rbCanny.isChecked():
                # Визуально выделяем границы
                thresholded_mat = cv2.Canny(thresholded_mat, 100, 50, 5)

            if self.ui.rbResult.isChecked():
                # Находим контуры
                _, countours, hierarchy = cv2.findContours(
                    thresholded_mat,
                    cv2.RETR_TREE,
                    # cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE
                )

                result_img = self.numpy_array_to_QImage(self.m_mat)

                p = Qt.QPainter(result_img)
                p.setPen(Qt.QPen(Qt.Qt.green, 2))

                for i, c in enumerate(countours):
                    x, y, width, height = cv2.boundingRect(c)
                    p.drawRect(x, y, width, height)

                p.end()

            else:
                result_img = self.numpy_array_to_QImage(thresholded_mat)

        size = self.ui.lbView.size()
        pixmap = Qt.QPixmap.fromImage(result_img).scaled(size, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation)
        self.ui.lbView.setPixmap(pixmap)

    def closeEvent(self, e):
        for w in self.findChildren(Qt.QSlider):
            name = w.objectName()
            self.m_settings.setValue(name, w.value())


if __name__ == '__main__':
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
