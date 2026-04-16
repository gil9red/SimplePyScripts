#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from api.common import Video


url = "https://www.youtube.com/watch?v=rgYQ7nUulAQ"
video = Video.get_from(url)

transcripts = video.get_transcripts()
assert len(transcripts)
print(f"Transcripts ({len(transcripts)}):")
print(*transcripts[:3], sep="\n")
print("...")
print(*transcripts[-3:], sep="\n")
"""
Transcripts (275):
TranscriptItem(start_ms=8840, end_ms=14219, start_time_str='0:08', text="hi everybody\n\nI'm Jesse wykel and I'm a front-end")
TranscriptItem(start_ms=14219, end_ms=21029, start_time_str='0:14', text="developer and this is my first live\n\nstream for free code camp I've done some")
TranscriptItem(start_ms=21029, end_ms=28949, start_time_str='0:21', text='live streams on my own channel but this\n\nis the first one on free code camp which')
...
TranscriptItem(start_ms=1908679, end_ms=1915690, start_time_str='31:48', text="if there's any tips for me I'm still\n\npretty new at this live-streaming thing\n\nso definitely any tips are are very")
TranscriptItem(start_ms=1915690, end_ms=1920950, start_time_str='31:55', text="welcome all right so I'll end the stream")
TranscriptItem(start_ms=1920950, end_ms=1928329, start_time_str='32:00', text="now thanks again have a great day I'll\n\nbe back tomorrow\n\n[Music]")
"""
