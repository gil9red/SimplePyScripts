#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        from PySide.QtCore import QCoreApplication, QEventLoop
        from PySide.phonon import Phonon

        app = QCoreApplication(sys.argv)

        audio = Phonon.MediaObject()
        audio.setCurrentSource(Phonon.MediaSource(''))
        output = Phonon.AudioOutput(Phonon.MusicCategory)
        Phonon.createPath(audio, output)

        file_name = sys.argv[1]
        audio.setCurrentSource(Phonon.MediaSource(file_name))
        audio.play()

        loop = QEventLoop()
        audio.finished.connect(loop.quit)
        loop.exec_()

    else:
        import os
        file_name = os.path.basename(sys.argv[0])
        print('usage: {} [-h] audio_file_name'.format(file_name))
