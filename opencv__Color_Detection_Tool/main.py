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

        self.settings = Qt.QSettings(CONFIG_FILE_NAME, Qt.QSettings.IniFormat)
        self.last_load_path = self.settings.value("lastLoadPath", ".")
        self.image_source = None

        for w in self.findChildren(Qt.QSlider):
            w.sliderMoved.connect(self.refresh_HSV)

            name = w.objectName()
            w.setValue(int(self.settings.value(name, w.value())))
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
        file_name = Qt.QFileDialog.getOpenFileName(self, "Load image", self.last_load_path, "Images (*.jpg *.jpeg *.png *.bmp)")[0]
        if not file_name:
            return

        self.last_load_path = Qt.QFileInfo(file_name).absolutePath()

        # TODO: плохо работает с изображениями с прозрачностью
        self.image_source = cv2.imread(file_name)
        # self.image_source = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
        self.image_source = cv2.cvtColor(self.image_source, cv2.COLOR_BGR2RGB)

        self.refresh_HSV()
    
    @staticmethod
    def numpy_array_to_QImage(numpy_array):
        gray_color_table = [Qt.qRgb(i, i, i) for i in range(256)]

        if numpy_array.dtype == np.uint8:
            if len(numpy_array.shape) == 2:
                img = Qt.QImage(numpy_array.data, numpy_array.shape[1], numpy_array.shape[0], numpy_array.strides[0], Qt.QImage.Format_Indexed8)
                img.setColorTable(gray_color_table)
                return img

            elif len(numpy_array.shape) == 3:
                if numpy_array.shape[2] == 3:
                    img = Qt.QImage(numpy_array.data, numpy_array.shape[1], numpy_array.shape[0], numpy_array.strides[0], Qt.QImage.Format_RGB888)
                    return img

                elif numpy_array.shape[2] == 4:
                    img = Qt.QImage(numpy_array.data, numpy_array.shape[1], numpy_array.shape[0], numpy_array.strides[0], Qt.QImage.Format_ARGB32)
                    return img

        # if len(numpy_array.shape) == 3:
        #     height, width, channel = numpy_array.shape
        #     bytes_per_line = 3 * width
        #     return Qt.QImage(numpy_array.data, width, height, bytes_per_line, Qt.QImage.Format_RGB888)
        # else:
        #     height, width = numpy_array.shape
        #     bytes_per_line = 1 * width
        #     return Qt.QImage(numpy_array.data, width, height, bytes_per_line, Qt.QImage.Format_Indexed8)
    
    def refresh_HSV(self):
        if self.image_source is None:
            return

        if self.ui.rbOriginal.isChecked():
            result_img = self.numpy_array_to_QImage(self.image_source)

        else:
            hue_from = self.ui.slHueFrom.value()
            hue_to = max(hue_from, self.ui.slHueTo.value())

            saturation_from = self.ui.slSaturationFrom.value()
            saturation_to = max(saturation_from, self.ui.slSaturationTo.value())

            value_from = self.ui.slValueFrom.value()
            value_to = max(value_from, self.ui.slValueTo.value())

            thresholded_image = cv2.cvtColor(self.image_source, cv2.COLOR_RGB2HSV)

            hsv_min = hue_from, saturation_from, value_from
            hsv_max = hue_to, saturation_to, value_to

            # TODO: под слайдерами показывать пример цвета с hsv_min и hsv_max

            # Отфильтровываем только то, что нужно, по диапазону цветов
            thresholded_image = cv2.inRange(
                thresholded_image,
                np.array(hsv_min, np.uint8),
                np.array(hsv_max, np.uint8)
            )

            # Убираем шум
            thresholded_image = cv2.erode(
                thresholded_image,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )
            thresholded_image = cv2.dilate(
                thresholded_image,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )

            # Замыкаем оставшиеся крупные объекты
            thresholded_image = cv2.dilate(
                thresholded_image,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )
            thresholded_image = cv2.erode(
                thresholded_image,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )

            if self.ui.rbCanny.isChecked():
                # Визуально выделяем границы
                thresholded_image = cv2.Canny(thresholded_image, 100, 50, 5)

            if self.ui.rbResult.isChecked():
                # Находим контуры
                _, countours, hierarchy = cv2.findContours(
                    thresholded_image,
                    cv2.RETR_TREE,
                    # cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE
                )

                result_img = self.numpy_array_to_QImage(self.image_source)

                p = Qt.QPainter(result_img)
                p.setPen(Qt.QPen(Qt.Qt.green, 2))

                for i, c in enumerate(countours):
                    x, y, width, height = cv2.boundingRect(c)
                    p.drawRect(x, y, width, height)

                p.end()

            else:
                result_img = self.numpy_array_to_QImage(thresholded_image)

        size = self.ui.lbView.size()
        pixmap = Qt.QPixmap.fromImage(result_img).scaled(size, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation)
        self.ui.lbView.setPixmap(pixmap)

    def closeEvent(self, e):
        for w in self.findChildren(Qt.QSlider):
            name = w.objectName()
            self.settings.setValue(name, w.value())

        self.settings.setValue("lastLoadPath", self.last_load_path)


if __name__ == '__main__':
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
