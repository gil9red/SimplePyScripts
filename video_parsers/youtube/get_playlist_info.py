#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from api.common import Playlist, session, get_yt_initial_data


url = "https://www.youtube.com/playlist?list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r"
assert Playlist.get_id_from_url(url) == "PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r"

url = "http://www.youtube.com/playlist?list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&feature=applinks"
assert Playlist.get_id_from_url(url) == "PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r"

url_playlist = (
    "https://www.youtube.com/playlist?list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r"
)
rs = session.get(url_playlist)
data = get_yt_initial_data(rs.text)
playlist_title = Playlist.get_title(data)
print(f"Playlist title: {playlist_title!r}")
# Playlist title: 'Live Coding with Jesse'

print()

playlist_v1 = Playlist.get_from("PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r")
print(f"playlist_v1: {playlist_v1}")
print(
    f"playlist_v1. Video ({len(playlist_v1.video_list)}):\n"
    f"    First: {playlist_v1.video_list[0]}\n"
    f"    Last:  {playlist_v1.video_list[-1]}"
)

print()

playlist_v2 = Playlist.get_from(url_playlist)
print(f"playlist_v2: {playlist_v1}")
print(
    f"playlist_v2. Video ({len(playlist_v2.video_list)}):\n"
    f"    First: {playlist_v2.video_list[0]}\n"
    f"    Last:  {playlist_v2.video_list[-1]}"
)

assert playlist_v1.id == playlist_v2.id
assert playlist_v1.title == playlist_v2.title
assert playlist_v1.duration_seconds == playlist_v2.duration_seconds
assert playlist_v1.duration_text == playlist_v2.duration_text
assert len(playlist_v1.video_list) == len(playlist_v2.video_list)
assert playlist_v1.video_list == playlist_v2.video_list

print("\n" + "-" * 100 + "\n")

# Getting "playlist" from url video
url_video = "https://www.youtube.com/watch?v=m1bPr3FRV1w&list=PLgqDz7CZ-6NbDjtcYuPFW2wb2LS7BQJMb&index=3"
print(f"From url video: {url_video}")
print(Playlist.get_from(url_video))
print()

url_video = "https://youtu.be/LSkNXxwrjLg?list=PLscFx0v8PvufteVzSldK135ymdvxncLEe"
playlist = Playlist.get_from(url_video)
print(f"From short url video: {url_video}")
print(Playlist.get_from(url_video))
