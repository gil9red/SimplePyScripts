#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import (
    QWidget, QSlider, QLabel, QToolButton,
    QStyle, QHBoxLayout, QVBoxLayout, QListWidget, QMessageBox,
    QListWidgetItem, QProgressBar
)
from PyQt5.QtGui import qFuzzyCompare, QKeyEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QUrl

from common import log


class PlayerControls(QWidget):
    """Класс описывает виджет с медийными кнопками."""

    play_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    stop_signal = pyqtSignal()
    next_signal = pyqtSignal()
    previous_signal = pyqtSignal()
    change_volume_signal = pyqtSignal(int)
    change_muting_signal = pyqtSignal(bool)

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

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(layout)
        main_layout.addLayout(layout_buttons)
        self.setLayout(main_layout)

        for tool_button in self.findChildren(QToolButton):
            tool_button.setAutoRaise(True)

    def _position_changed(self, pos):
        # TODO: с этим условием при кликах на тело слайдера, ползунок слайдера сдвинется
        # но медиа не будет перемотано
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

    def mute_clicked(self, _=None):
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


class LoadAudioListThread(QThread):
    """Класс потока для загрузки списка аудизаписей vk.com"""

    about_add_audio = pyqtSignal(str, str)
    about_progress = pyqtSignal(int)
    about_range_progress = pyqtSignal(int, int)

    def __init__(self, vk=None):
        super().__init__()

        self.vk = vk
        self._is_run = False

    def run(self):
        log.debug('Start thread.')

        try:
            # Выполняем запрос к vk, чтобы получить список аудизаписей
            rs = self.vk.method('audio.get')

            # TODO: за один запрос vk может и не выдать все аудизаписи
            audio_list = rs['items']

            self.about_range_progress.emit(0, len(audio_list))

            for i, audio in enumerate(audio_list, 0):
                if not self._is_run:
                    break

                try:
                    artist = audio['artist'].strip().title()
                    title = audio['title'].strip().capitalize()
                    title = artist + ' - ' + title
                    url = audio['url']

                    self.about_progress.emit(i)
                    self.about_add_audio.emit(title, url)

                except Exception as e:
                    log.exception('Error: {}, audio id={} owner_id={}'.format(e, audio['id'], audio['owner_id']))

        finally:
            log.debug('Finish thread.')

    def start(self, priority=QThread.InheritPriority):
        self._is_run = True

        super().start(priority)

    def exit(self, return_code=0):
        self._is_run = False

        return super().exit(return_code)


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

        if not self.player.isAvailable():
            # TODO: перевод
            text = "The QMediaPlayer object does not have a valid service.\n" \
                   "Please check the media service plugins are installed."

            log.warning(text)
            QMessageBox.warning(self, "Service not available", text)

            quit()

        self.controls = PlayerControls(self.player)
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

        self.progress = QProgressBar()
        self.progress.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.controls)
        layout.addWidget(self.audio_list_widget)
        layout.addWidget(self.progress)

        self.setLayout(layout)

        self.thread = LoadAudioListThread()
        self.thread.about_add_audio.connect(self._add_audio)
        self.thread.about_progress.connect(self.progress.setValue)
        self.thread.about_range_progress.connect(self.progress.setRange)
        self.thread.started.connect(self._start)
        self.thread.finished.connect(self._finished)

    def _add_audio(self, title, url):
        item = QListWidgetItem(title)
        item.setData(Qt.UserRole, url)
        self.audio_list_widget.addItem(item)
        self.playlist.addMedia(QMediaContent(QUrl(url)))

        # При добавлении первой аудизаписи, вызываем воспроизведение
        if self.audio_list_widget.count() == 1:
            self.audio_list_widget.setCurrentRow(0)
            self.playlist.setCurrentIndex(0)
            self.play()

    def _start(self):
        self.audio_list_widget.clear()
        self.playlist.clear()

        self.progress.show()

    def _finished(self):
        self.progress.hide()

    def fill(self, vk):
        self.thread.vk = vk

        # Если поток запущен, останавливаем его, иначе -- запускаем
        if self.thread.isRunning():
            self.thread.exit()
        else:
            self.thread.start()

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
