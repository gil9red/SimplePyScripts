__author__ = 'ipetrash'


from PySide.QtGui import *
import urllib.request
import re
import os


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.le_url = QLineEdit()
        self.le_url.setPlaceholderText("Url страницы с видео")
        self.le_url.setText("http://www.trahun.tv/video-studentki-lesbiyanki-s-malenkimi-soskami.html")

        self.pb_download = QPushButton("Скачать")
        self.pb_download.clicked.connect(self.slot_download)

        self.lw_log = QPlainTextEdit()

        layout = QHBoxLayout()
        layout.addWidget(self.le_url)
        layout.addWidget(self.pb_download)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.lw_log)
        self.setLayout(main_layout)

    def slot_download(self):
        url = self.le_url.text()
        # Скачивать будем в документы пользователя в папку Trahun
        dir = QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation)
        dir = os.path.join(dir, "Trahun")
        dir = os.path.normpath(dir)
        with urllib.request.urlopen(url) as f:  # Open url
            data = f.read()  # Download context url
            data = data.decode("utf-8")  # Bytes to str
            pattern = r"video_url=(.*?\.flv)"  # Pattern url video
            result = re.search(pattern, data)  # Search link to video :)
            url_video = result.group(1)  # Get one group -- url video
            base_name = os.path.basename(url_video)  # base name file video
            if not os.path.exists(dir):  # If dir not exist, then make
                os.makedirs(dir)
            file_name = os.path.join(dir, base_name)

            print("URL: %s" % url_video)
            print("Dir: %s" % dir)
            print("File: %s" % file_name)
            urllib.request.urlretrieve(url_video, file_name, reporthook=self.progress)

    def progress(self, count, block_size, total_size):
        percent = count * block_size * 100.0 / total_size
        print("Прогресс: {}/{}({:3.1f}%)".format(self.sizeof_fmt(count * block_size),
                                                 self.sizeof_fmt(total_size),
                                                 percent) + ' ' * 20,
                                                 end='\r')

    # Code from: http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    def sizeof_fmt(self, num):
        for x in ['bytes', 'KB', 'MB', 'GB']:
            if num < 1024.0:
                return "%3.1f%s" % (num, x)
            num /= 1024.0
        return "%3.1f%s" % (num, 'TB')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    w = Window()
    w.setWindowTitle("Пример 4")
    w.show()

    sys.exit(app.exec_())