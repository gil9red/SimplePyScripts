#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        from main import play
        play(sys.argv[1])

    else:
        import os
        file_name = os.path.basename(sys.argv[0])
        print('usage: {} [-h] audio_file_name'.format(file_name))
