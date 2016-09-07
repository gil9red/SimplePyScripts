#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Simple audio player vk.com"""


import sys
import traceback
import logging


def get_logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    fh = logging.FileHandler('log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


log = get_logger()


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    log.critical(text)
    QMessageBox.critical(None, 'Error', text)
    quit()

sys.excepthook = log_uncaught_exceptions


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

import vk_api


class AuthPage(QWidget):
    """Виджет предоставляет собой страницу авторизации."""

    about_successful_auth = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Объект для работы с vk api
        self.vk = None

        self.login = QLineEdit()
        self.login.returnPressed.connect(self.send_auth)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.send_auth)

        self.ok_button = QPushButton('Ok')
        self.ok_button.setDefault(True)
        self.ok_button.clicked.connect(self.send_auth)

        form_layout = QFormLayout()
        form_layout.addRow('Login:', self.login)
        form_layout.addRow('Password:', self.password)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.ok_button)
        layout.addStretch()

        self.setLayout(layout)

    def send_auth(self):
        login, password = self.login.text(), self.password.text()
        if not login or not password:
            QMessageBox.warning(self, 'Warning', 'Login or password is empty!')
            return

        # Пытаемся авторизоваться
        try:
            self.vk = vk_api.VkApi(login, password)
            self.vk.authorization()

        except Exception as e:
            QMessageBox.warning(self, 'Warning', 'Fail to authorize:\n' + str(e))
            return

        self.about_successful_auth.emit()


class PlayerControls(QWidget):
    """Класс описывает виджет с медийными кнопками."""

    play_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    stop_signal = pyqtSignal()
    next_signal = pyqtSignal()
    previous_signal = pyqtSignal()
    change_volume_signal = pyqtSignal(int)
    change_muting_signal = pyqtSignal(bool)
    # change_rate_signal = pyqtSignal(float)

    def __init__(self, player):
        super().__init__()

        self.player_state = QMediaPlayer.StoppedState
        self.player_muted = False

        self.player_slider = QSlider(Qt.Horizontal)
        self.player_slider.sliderMoved.connect(lambda secs: player.setPosition(secs * 1000))

        self.label_duration = QLabel()
        player.durationChanged.connect(lambda duration: self.player_slider.setRange(0, duration // 1000))
        player.positionChanged.connect(self._position_changed)

        player.stateChanged.connect(self.set_state)
        player.volumeChanged.connect(self.set_volume)
        player.mutedChanged.connect(self.set_muted)

        # TODO: добавить горячие клавиши для управления медиа
        self.play_pause_button = QToolButton()
        self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_pause_button.clicked.connect(self.play_clicked)

        self.stop_button = QToolButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_signal)

        self.next_button = QToolButton()
        self.next_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.next_button.clicked.connect(self.next_signal)

        self.previous_button = QToolButton()
        self.previous_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.previous_button.clicked.connect(self.previous_signal)

        self.mute_button = QToolButton()
        self.mute_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.mute_button.clicked.connect(self.mute_clicked)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.sliderMoved.connect(self.change_volume_signal)

        # self.rate_box = QComboBox()
        # self.rate_box.addItem("0.5x", 0.5)
        # self.rate_box.addItem("1.0x", 1.0)
        # self.rate_box.addItem("2.0x", 2.0)
        # self.rate_box.setCurrentIndex(1)
        # self.rate_box.activated.connect(self.update_rate)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.player_slider)
        layout.addWidget(self.label_duration)

        layout_buttons = QHBoxLayout()
        layout_buttons.setContentsMargins(0, 0, 0, 0)
        layout_buttons.setSpacing(0)
        layout_buttons.addWidget(self.stop_button)
        layout_buttons.addWidget(self.previous_button)
        layout_buttons.addWidget(self.play_pause_button)
        layout_buttons.addWidget(self.next_button)
        layout_buttons.addWidget(self.mute_button)
        layout_buttons.addWidget(self.volume_slider)
        # layout_buttons.addWidget(self.rate_box)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(layout)
        main_layout.addLayout(layout_buttons)
        self.setLayout(main_layout)

        for tool_button in self.findChildren(QToolButton):
            tool_button.setAutoRaise(True)

    def _position_changed(self, pos):
        # TODO: с этим условием при кликах на тело слайдера, ползунок слайдера сдвинется
        # но видео не будет перемотано
        if not self.player_slider.isSliderDown():
            self.player_slider.setValue(pos / 1000)

        self._update_duration_info()

    def _update_duration_info(self):
        ms_pattern = "{:0>2}:{:0>2}"
        hms_pattern = "{}:" + ms_pattern

        seconds = self.player_slider.value()
        current_minutes, current_seconds = divmod(seconds, 60)
        current_hours, current_minutes = divmod(current_minutes, 60)
        if current_hours > 0:
            current = hms_pattern.format(current_hours, current_minutes, current_seconds)
        else:
            current = ms_pattern.format(current_minutes, current_seconds)

        total_seconds = self.player_slider.maximum()
        total_minutes, total_seconds = divmod(total_seconds, 60)
        total_hours, total_minutes = divmod(total_minutes, 60)
        if total_hours > 0:
            total = hms_pattern.format(total_hours, total_minutes, total_seconds)
        else:
            total = ms_pattern.format(total_minutes, total_seconds)

        self.label_duration.setText(current + ' / ' + total)

    def state(self):
        return self.player_state

    def set_state(self, state):
        if state != self.player_state:
            self.player_state = state

            if state == QMediaPlayer.StoppedState:
                self.stop_button.setEnabled(False)
                self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

            elif state == QMediaPlayer.PlayingState:
                self.stop_button.setEnabled(True)
                self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

            elif state == QMediaPlayer.PausedState:
                self.stop_button.setEnabled(True)
                self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def volume(self):
        return self.volume_slider.value()

    def set_volume(self, volume):
        self.volume_slider.setValue(volume)

    def is_muted(self):
        return self.player_muted

    def set_muted(self, muted):
        if muted != self.player_muted:
            self.player_muted = muted

            icon = QStyle.SP_MediaVolumeMuted if muted else QStyle.SP_MediaVolume
            self.mute_button.setIcon(self.style().standardIcon(icon))

    def play_clicked(self):
        if self.player_state == QMediaPlayer.StoppedState or self.player_state == QMediaPlayer.PausedState:
            self.play_signal.emit()

        elif self.player_state == QMediaPlayer.PlayingState:
            self.pause_signal.emit()

    def mute_clicked(self, is_mute=None):
        self.change_muting_signal.emit(not self.player_muted)

    def playback_rate(self):
        return self.rate_box.itemData(self.rate_box.currentIndex())

    def set_playback_rate(self, rate):
        for i in range(self.rate_box.count()):
            if qFuzzyCompare(rate, self.rate_box.itemData(i)):
                self.rate_box.setCurrentIndex(i)
                return

        self.rate_box.addItem("{}x".format(rate), rate)
        self.rate_box.setCurrentIndex(self.rate_box.count() - 1)

    def update_rate(self):
        self.change_rate_signal.emit(self.playback_rate())


class AudioPlayerPage(QWidget):
    about_play_audio = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.audio_list_widget = QListWidget()
        self.audio_list_widget.installEventFilter(self)
        self.audio_list_widget.itemDoubleClicked.connect(self.play)

        # TODO: playlist объединить с audio_list_widget (см примеры работы с QMediaPlayer)
        self.playlist = QMediaPlaylist()
        self.playlist.currentIndexChanged.connect(lambda row: self.audio_list_widget.setCurrentRow(row))

        # TODO: обрабатывать сигналы плеера: http://doc.qt.io/qt-5/qmediaplayer.html#signals
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.currentMediaChanged.connect(
            lambda media: self.about_play_audio.emit(self.audio_list_widget.currentItem().text()))

        self.controls = PlayerControls(self.player)

        # Скорость воспроизведения все-равно нельзя изменять
        # self.controls.rate_box.hide()

        self.controls.set_state(self.player.state())
        self.controls.set_volume(self.player.volume())
        self.controls.set_muted(self.controls.is_muted())

        self.controls.play_signal.connect(self.play)
        self.controls.pause_signal.connect(self.player.pause)
        self.controls.stop_signal.connect(self.player.stop)
        self.controls.next_signal.connect(self.playlist.next)
        self.controls.previous_signal.connect(self.playlist.previous)
        self.controls.change_volume_signal.connect(self.player.setVolume)
        self.controls.change_muting_signal.connect(self.player.setMuted)
        # self.controls.change_rate_signal.connect(self.player.setPlaybackRate)

        layout = QVBoxLayout()
        layout.addWidget(self.controls)
        layout.addWidget(self.audio_list_widget)

        self.setLayout(layout)

    def fill(self, vk):
        self.audio_list_widget.clear()
        self.playlist.clear()

        # TODO: засунуть в отдельный поток
        rs = vk.method('audio.get')

        for audio in rs['items']:
            try:
                artist = audio['artist'].strip().title()
                title = audio['title'].strip().capitalize()
                title = artist + ' - ' + title
                url = audio['url']

                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, url)
                self.audio_list_widget.addItem(item)

                self.playlist.addMedia(QMediaContent(QUrl(url)))

            except Exception as e:
                log.exception('Error: {}, audio id={} owner_id={}'.format(e, audio['id'], audio['owner_id']))

        if not self.player.isAvailable():
            # TODO: перевод
            QMessageBox.warning(self,
                                "Service not available",
                                "The QMediaPlayer object does not have a valid service.\n"
                                "Please check the media service plugins are installed.")

            self.controls.setEnabled(False)
            self.audio_list_widget.setEnabled(False)

        self.audio_list_widget.setCurrentRow(0)
        self.playlist.setCurrentIndex(0)

        self.play()

    def play(self):
        self.playlist.setCurrentIndex(self.audio_list_widget.currentRow())
        self.player.play()

    def eventFilter(self, obj, event):
        # Воспроизведение видео при клике на кнопки Enter/Return в плейлисте
        if obj == self.audio_list_widget and event.type() == QKeyEvent.KeyPress:
            if self.audio_list_widget.hasFocus() and event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                item = self.audio_list_widget.currentItem()
                if item is not None:
                    self.play()

        return super().eventFilter(obj, event)


TITLE = 'audio_player_vk'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.update_title()

        self.auth_page = AuthPage()
        self.auth_page.about_successful_auth.connect(self.go_audio_player_page)

        self.audio_player_page = AudioPlayerPage()
        self.audio_player_page.about_play_audio.connect(self.update_title)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.auth_page)
        self.stacked_widget.addWidget(self.audio_player_page)

        self.setCentralWidget(self.stacked_widget)

    def update_title(self, audio_title=''):
        self.setWindowTitle(TITLE + '. ' + audio_title)

    def go_audio_player_page(self):
        self.stacked_widget.setCurrentWidget(self.audio_player_page)

        vk = self.auth_page.vk
        self.audio_player_page.fill(vk)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
