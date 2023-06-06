#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re
import time
import traceback

from dataclasses import dataclass, field
from datetime import datetime
from typing import Generator, Callable, Any
from urllib.parse import urljoin, urlparse, parse_qs

# pip install tzlocal
import tzlocal

# pip install dpath
import dpath.util

import requests


class AlertError(Exception):
    pass


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/f0403620f7948306ad9e34a373f2aabc0237fb2a/seconds_to_str.py
def seconds_to_str(seconds: int) -> str:
    hh, mm = divmod(seconds, 3600)
    mm, ss = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


def time_to_seconds(time_str: str) -> int:
    time_split = list(map(int, time_str.split(":")))

    if len(time_split) == 3:
        h, m, s = time_split
        return h * 60 * 60 + m * 60 + s

    elif len(time_split) == 2:
        m, s = time_split
        return m * 60 + s

    else:
        return time_split[0]


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
)

BASE_URL = "https://www.youtube.com"

session = requests.Session()
session.headers["User-Agent"] = USER_AGENT


def download_url_as_bytes(url: str) -> bytes:
    rs = session.get(url)
    rs.raise_for_status()
    return rs.content


def get_yt_cfg_data(html: str) -> dict:
    m = re.search(r"ytcfg\.set\((\{.+?\})\);", html)
    if not m:
        raise Exception("Не удалось найти на странице ytcfg.set!")

    return json.loads(m.group(1))


def get_ytInitialData(html: str) -> dict | None:
    patterns = [
        re.compile(r'window\["ytInitialData"\] = (\{.+?\});'),
        re.compile(r"var ytInitialData = (\{.+?\});"),
    ]

    for pattern in patterns:
        m = pattern.search(html)
        if m:
            data_str = m.group(1)
            return json.loads(data_str)


def get_yt_initial_player_response(html: str) -> dict:
    m = re.search(r"ytInitialPlayerResponse = (\{.+?\});", html)
    if not m:
        raise Exception("Не удалось найти на странице ytInitialPlayerResponse!")

    return json.loads(m.group(1))


def raise_if_error(yt_initial_data: dict):
    # NOTE: Example:
    """
    ...
    "alerts": [
        {
            "alertRenderer": {
                "type": "ERROR",
                "text": {
                    "runs": [
                        {
                            "text": "Этот тип плейлиста недоступен для просмотра."
                        }
                    ]
                }
            }
        }
    ],
    ...
    """

    try:
        # NOTE: Старый вариант с dpath.util.values занимал в разы больше времени - на плейлисте с 150 видео
        #       уходило ~40 секунд, с новым вариантом ~4.5 секунды
        alerts = yt_initial_data.get("alerts")
        if not alerts:
            return

        for alert_obj in alerts:
            alert = alert_obj.get("alertRenderer")
            if not alert or alert["type"] != "ERROR":
                continue

            text = dpath.util.get(alert, "text/runs/0/text")
            raise AlertError(text)

    except KeyError:
        pass


@dataclass
class Context:
    data_video: dict = None
    yt_initial_data: dict = None
    yt_cfg_data: dict = None
    rs: requests.Response = None


@dataclass
class Thumbnail:
    url: str
    width: str
    height: str

    @classmethod
    def get_from(cls, thumbnail: dict) -> "Thumbnail":
        return cls(
            url=thumbnail["url"],
            width=thumbnail["width"],
            height=thumbnail["height"],
        )


@dataclass
class TranscriptItem:
    start_ms: int
    end_ms: int
    start_time_str: str
    text: str

    @classmethod
    def get_from(cls, transcript_segment_renderer: dict) -> "TranscriptItem":
        return cls(
            start_ms=int(transcript_segment_renderer["startMs"]),
            end_ms=int(transcript_segment_renderer["endMs"]),
            start_time_str=dpath.util.get(
                transcript_segment_renderer, "startTimeText/simpleText"
            ),
            text=dpath.util.get(transcript_segment_renderer, "**/runs/0/text"),
        )


@dataclass
class Video:
    id: str
    url: str
    title: str
    duration_seconds: int = None
    duration_text: str = None
    seq: int = None
    is_live_now: bool = False
    thumbnails: list[Thumbnail] = field(default_factory=list, repr=False, compare=False)
    context: Context = field(default=None, repr=False, compare=False)

    @classmethod
    def parse_url(cls, data_video: dict) -> str:
        url_video = dpath.util.get(
            data_video, "navigationEndpoint/commandMetadata/webCommandMetadata/url"
        )
        return urljoin(BASE_URL, url_video)

    @classmethod
    def parse_title(cls, data_video: dict) -> str:
        if title := data_video.get("title"):
            if title and isinstance(title, str):
                return title

        try:
            return dpath.util.get(data_video, "title/runs/0/text")
        except KeyError:
            return dpath.util.get(data_video, "title/simpleText")

    @classmethod
    def parse_duration_seconds(cls, data_video: dict) -> int:
        # Если есть продолжительность в секундах
        try:
            duration_seconds = int(data_video["lengthSeconds"])
        except KeyError:
            # Если есть продолжительность в секундах в виде текста, пробуем распарсить
            try:
                text = dpath.util.get(data_video, "lengthText/simpleText")
                duration_seconds = time_to_seconds(text)
            except KeyError:
                duration_seconds = None

        return duration_seconds

    def get_url_thumbnail_by_max_size(self) -> str:
        return max(self.thumbnails, key=lambda x: (x.width, x.height)).url

    def get_url_thumbnail_for_maxresdefault(self) -> str:
        url = self.get_url_thumbnail_by_max_size()

        # Replacing last part from path on maxresdefault.jpg
        # https://i.ytimg.com/vi/4ewTMva83tQ/hqdefault.jpg?sqp=-oaymwEbCKgBEF5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLA8lXazyahcoE7chGgA-ZjYZQ6wcw
        #   -> https://i.ytimg.com/vi/4ewTMva83tQ/maxresdefault.jpg
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split("/")
        path_parts[-1] = "maxresdefault.jpg"
        new_path = "/".join(path_parts)
        parsed_url = parsed_url._replace(query="", path=new_path)

        return parsed_url.geturl()

    def get_thumbnail_by_max_size(self) -> bytes:
        return download_url_as_bytes(self.get_url_thumbnail_by_max_size())

    def get_thumbnail_for_maxresdefault(self) -> bytes:
        return download_url_as_bytes(self.get_url_thumbnail_for_maxresdefault())

    @classmethod
    def get_is_live_now(cls, video: dict) -> bool:
        # Стримы имеют значок BADGE_STYLE_TYPE_LIVE_NOW
        try:
            badges = dpath.util.values(video, "**/metadataBadgeRenderer/style")
            return "BADGE_STYLE_TYPE_LIVE_NOW" in badges
        except KeyError:
            pass

        return False

    @classmethod
    def parse_from(
        cls,
        data_video: dict,
        parent_context: Context = None,
        url_video: str = "",
    ) -> "Video":
        if parent_context and parent_context.yt_initial_data:
            raise_if_error(parent_context.yt_initial_data)

        title = cls.parse_title(data_video)

        if not url_video:
            url_video = cls.parse_url(data_video)

        duration_seconds = cls.parse_duration_seconds(data_video)

        duration_text = None
        if duration_seconds:
            duration_text = seconds_to_str(duration_seconds)

        try:
            seq = int(data_video["index"]["simpleText"])
        except:
            seq = None

        thumbnails = [
            Thumbnail.get_from(thumbnail)
            for thumbnail in dpath.util.values(data_video, "thumbnail/thumbnails/*")
        ]

        context = Context(data_video=data_video)
        if parent_context:
            context.yt_initial_data = parent_context.yt_initial_data
            context.yt_cfg_data = parent_context.yt_cfg_data
            context.rs = parent_context.rs

        return cls(
            id=data_video["videoId"],
            url=url_video,
            title=title,
            duration_seconds=duration_seconds,
            duration_text=duration_text,
            seq=seq,
            is_live_now=cls.get_is_live_now(data_video),
            thumbnails=thumbnails,
            context=context,
        )

    @classmethod
    def get_id_from_url(cls, url: str) -> str:
        parsed_url = urlparse(url)
        return parse_qs(parsed_url.query)["v"][0]

    @classmethod
    def get_url(cls, video_id: str) -> str:
        return urljoin(BASE_URL, f"watch?v={video_id}")

    @classmethod
    def get_from(cls, url_or_id: str) -> "Video":
        if url_or_id.startswith("http"):
            url = url_or_id
        else:
            url = cls.get_url(url_or_id)

        rs, yt_initial_data = load(url)
        raise_if_error(yt_initial_data)

        # NOTE: Оригинальный url может поменяться, лучше брать тот, что будет после запроса
        url = rs.url

        yt_cfg_data = get_yt_cfg_data(rs.text)
        context = Context(
            yt_initial_data=yt_initial_data,
            yt_cfg_data=yt_cfg_data,
            rs=rs,
        )

        data_video = dpath.util.get(yt_initial_data, "**/videoPrimaryInfoRenderer")
        yt_initial_player_response = get_yt_initial_player_response(rs.text)

        # NOTE: Костыль, чтобы старый код, парсящий видео из плейлистов и других страниц,
        #       в parse_from смог разобрать
        dict_merge(data_video, yt_initial_player_response["videoDetails"])

        return cls.parse_from(
            data_video=data_video,
            parent_context=context,
            url_video=url,
        )

    def get_transcripts(self) -> list[TranscriptItem]:
        yt_cfg_data = self.context.yt_cfg_data
        innertube_api_key = yt_cfg_data["INNERTUBE_API_KEY"]
        context = get_context_data(self.url, yt_cfg_data["INNERTUBE_CONTEXT"])

        params_get_transcript_endpoint = dpath.util.get(
            self.context.yt_initial_data,
            "**/content/continuationItemRenderer/continuationEndpoint/getTranscriptEndpoint/params",
            default=None,
        )
        if not params_get_transcript_endpoint:
            return []

        context["params"] = params_get_transcript_endpoint

        url = f"{BASE_URL}/youtubei/v1/get_transcript"
        params = {
            "key": innertube_api_key,
            "prettyPrint": "false",
        }
        rs = session.post(url, json=context, params=params)
        rs_data = rs.json()

        transcript_items = dpath.util.values(rs_data, "**/transcriptSegmentRenderer")
        return [TranscriptItem.get_from(item) for item in transcript_items]


@dataclass
class Playlist:
    id: str
    url: str
    title: str
    video_list: list[Video] = field(default_factory=list, repr=False)
    duration_seconds: int = None
    duration_text: str = None
    context: Context = field(default=None, repr=False, compare=False)

    @classmethod
    def get_id_from_url(cls, url: str) -> str:
        parsed_url = urlparse(url)
        return parse_qs(parsed_url.query)["list"][0]

    @classmethod
    def get_url(cls, playlist_id: str) -> str:
        return urljoin(BASE_URL, f"playlist?list={playlist_id}")

    @classmethod
    def get_title(cls, yt_initial_data: dict) -> str:
        try:
            # Playlist
            return dpath.util.get(
                yt_initial_data, "**/metadata/playlistMetadataRenderer/title"
            )
        except KeyError:
            try:
                # Mix
                return dpath.util.get(yt_initial_data, "**/playlist/playlist/title")
            except KeyError:
                return dpath.util.get(yt_initial_data, "title/simpleText")

    @classmethod
    def get_from(cls, url_or_id: str) -> "Playlist":
        if url_or_id.startswith("http"):
            url = url_or_id
            playlist_id = cls.get_id_from_url(url)

            # Extracting playlist url from url video
            if "/watch?" in url:
                url = cls.get_url(playlist_id)

        else:
            playlist_id = url_or_id
            url = cls.get_url(playlist_id)

        rs, yt_initial_data = load(url)

        raise_if_error(yt_initial_data)

        # NOTE: Оригинальный url может поменяться, лучше брать тот, что будет после запроса
        url = rs.url

        context = Context(
            yt_initial_data=yt_initial_data,
            rs=rs,
        )

        title = cls.get_title(yt_initial_data)

        total_seconds = 0
        video_list = []
        for data_video in get_generator_raw_video_list_from_data(yt_initial_data, rs):
            video = Video.parse_from(data_video, context)
            video_list.append(video)

            if video.duration_seconds:
                total_seconds += video.duration_seconds

        return cls(
            id=playlist_id,
            url=url,
            title=title,
            video_list=video_list,
            duration_seconds=total_seconds,
            duration_text=seconds_to_str(total_seconds),
            context=context,
        )


def dict_merge(d1: dict, d2: dict):
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):
            dict_merge(d1[k], v)
        else:
            d1[k] = v


def get_context_data(url: str, innertube_context: dict) -> dict:
    local_zone = tzlocal.get_localzone()
    utc_offset_minutes = local_zone.utcoffset(datetime.now()).total_seconds() // 60

    context_data = {
        "context": {
            "client": {
                "hl": "ru",
                "gl": "RU",
                "remoteHost": "",
                "deviceMake": "",
                "deviceModel": "",
                "visitorData": "",
                "userAgent": f"{USER_AGENT},gzip(gfe)",
                "clientName": "WEB",
                "clientVersion": "2.20210816.01.00",
                "osName": "Windows",
                "osVersion": "10.0",
                "originalUrl": url,
                "platform": "DESKTOP",
                "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                "timeZone": str(local_zone),
                "browserName": "Firefox",
                "browserVersion": "91.0",
                "screenWidthPoints": 1280,
                "screenHeightPoints": 548,
                "screenPixelDensity": 1,
                "screenDensityFloat": 1,
                "utcOffsetMinutes": utc_offset_minutes,
                "mainAppWebInfo": {
                    "graftUrl": url,
                    "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                    "isWebNativeShareAvailable": False,
                },
            },
            "user": {"lockedSafetyMode": False},
            "request": {
                "useSsl": True,
                "internalExperimentFlags": [],
                "consistencyTokenJars": [],
            },
            "adSignalsInfo": {
                "params": [
                    {"key": "dt", "value": ""},
                    {"key": "flash", "value": "0"},
                    {"key": "frm", "value": "0"},
                    {"key": "u_tz", "value": "300"},
                    {"key": "u_his", "value": "1"},
                    {"key": "u_java", "value": "false"},
                    {"key": "u_h", "value": "1024"},
                    {"key": "u_w", "value": "1280"},
                    {"key": "u_ah", "value": "984"},
                    {"key": "u_aw", "value": "1280"},
                    {"key": "u_cd", "value": "24"},
                    {"key": "u_nplug", "value": "0"},
                    {"key": "u_nmime", "value": "0"},
                    {"key": "bc", "value": "31"},
                    {"key": "bih", "value": "548"},
                    {"key": "biw", "value": "1263"},
                    {
                        "key": "brdim",
                        "value": "-1288,40,-1288,40,1280,48,1296,1000,1280,548",
                    },
                    {"key": "vis", "value": "1"},
                    {"key": "wgl", "value": "true"},
                    {"key": "ca_type", "value": "image"},
                ]
            },
        },
    }

    dict_merge(context_data["context"], innertube_context)

    return context_data


def get_data_for_next_page(
    url: str, yt_cfg_data: dict, continuation_item: dict
) -> dict:
    innertube_context = yt_cfg_data.get("INNERTUBE_CONTEXT")
    if not innertube_context:
        raise Exception("Значение INNERTUBE_CONTEXT должно быть задано в yt_cfg_data!")

    click_tracking_params = continuation_item["continuationEndpoint"]["clickTrackingParams"]
    continuation_token = continuation_item["continuationEndpoint"]["continuationCommand"]["token"]

    pattern_next_page_data = get_context_data(url, innertube_context)
    pattern_next_page_data["continuation"] = continuation_token
    pattern_next_page_data["context"]["clickTracking"] = {
        "clickTrackingParams": click_tracking_params,
    }

    return pattern_next_page_data


def load(url: str) -> tuple[requests.Response, dict]:
    rs = session.get(url)

    data = get_ytInitialData(rs.text)
    if not data:
        raise Exception("Could not find ytInitialData!")

    return rs, data


def get_raw_video_renderer_items(yt_initial_data: dict) -> list[dict]:
    items = []
    for render in [
        "**/gridVideoRenderer",
        "**/videoRenderer",
        "**/playlistVideoRenderer",
        "**/playlistPanelVideoRenderer",
        "**/playlistRenderer",
    ]:
        items += dpath.util.values(yt_initial_data, render)

    return items


def get_generator_raw_video_list_from_data(
    yt_initial_data: dict, rs: requests.Response
) -> Generator[dict, None, None]:
    yt_cfg_data = get_yt_cfg_data(rs.text)
    innertube_api_key = yt_cfg_data["INNERTUBE_API_KEY"]

    # Первая порция видео будет в самой странице
    yield from get_raw_video_renderer_items(yt_initial_data)

    data = yt_initial_data

    # Подгрузка следующих видео
    while True:
        time.sleep(0.5)

        try:
            continuation_item = dpath.util.get(data, "**/continuationItemRenderer")
        except KeyError:
            break
        except ValueError:
            # TODO: fix it for "Mix"
            # Ignore
            print("Warning:\n" + traceback.format_exc())
            break

        url_next_page_data = urljoin(
            rs.url, dpath.util.get(continuation_item, "**/webCommandMetadata/apiUrl")
        )

        next_page_data = get_data_for_next_page(rs.url, yt_cfg_data, continuation_item)
        rs = session.post(
            url_next_page_data, params={"key": innertube_api_key}, json=next_page_data
        )
        data = rs.json()

        yield from get_raw_video_renderer_items(data)


def get_generator_raw_video_list(url: str) -> Generator[dict, None, None]:
    rs, data = load(url)
    yield from get_generator_raw_video_list_from_data(data, rs)


def get_raw_video_list(url: str, maximum_items=1000) -> list[dict]:
    items = []
    for i, video in enumerate(get_generator_raw_video_list(url)):
        if i >= maximum_items:
            break

        items.append(video)

    return items


def get_video_list(url: str, *args, **kwargs) -> list[Video]:
    return [
        Video.parse_from(video)
        for video in get_raw_video_list(url, *args, **kwargs)
        if "videoId" in video  # NOTE: У плейлистов будет playlistId
    ]


def search_youtube(text_or_url: str, *args, **kwargs) -> list[Video]:
    if text_or_url.startswith("http"):
        url = text_or_url
    else:
        text = text_or_url
        url = urljoin(BASE_URL, f"results?search_query={text}")

    return get_video_list(url, *args, **kwargs)


def search_youtube_with_filter(
    url: str, sort=False, filter_func: Callable[[Any], bool] = None
) -> list[str]:
    video_title_list = [video.title for video in search_youtube(url)]
    if sort:
        video_title_list.sort()

    if callable(filter_func):
        video_title_list = list(filter(filter_func, video_title_list))

    return video_title_list


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=rgYQ7nUulAQ"
    video_id = Video.get_id_from_url(url)
    assert video_id == "rgYQ7nUulAQ"

    new_url = Video.get_url(video_id)
    assert url == new_url

    video = Video.get_from(url)
    print(video)
    print()
    # Video(id='rgYQ7nUulAQ', url='https://www.youtube.com/watch?v=rgYQ7nUulAQ', title='Building a Website (P1D2) - Live Coding with Jesse', duration_seconds=1929, duration_text='00:32:09', seq=None, is_live_now=False)

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

    print("\n" + "-" * 100 + "\n")

    url = "https://www.youtube.com/playlist?list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r"
    assert Playlist.get_id_from_url(url) == "PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r"

    url = "http://www.youtube.com/playlist?list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&feature=applinks"
    assert Playlist.get_id_from_url(url) == "PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r"

    url_playlist = "https://www.youtube.com/playlist?list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r"
    rs = session.get(url_playlist)
    data = get_ytInitialData(rs.text)
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
    print("From url video:")
    print(Playlist.get_from(url_video))

    print("\n" + "-" * 100 + "\n")

    def __print_video_list(items: list[Video]):
        print(f"Items ({len(items)}):")
        for i, video in enumerate(items, 1):
            print(f"  {i:3}. {video.title!r}: {video.url}")

    items = get_video_list(url_playlist)
    __print_video_list(items)
    """
    Items (226):
        1. 'Run freeCodeCamp Locally  (P8D2) - Live Coding with Jesse': https://www.youtube.com/watch?v=GFQ9VZYw2-0&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=1
        2. 'React Native Browser Editor  (P8D1) - Live Coding with Jesse': https://www.youtube.com/watch?v=drN9DEm3hFE&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=2
        3. 'React Native Web Styling Part 2  (P7D13) - Live Coding with Jesse': https://www.youtube.com/watch?v=VSLMJ2mZx5Y&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=3
        ...
      224. 'Material Design Cards - Live Coding with Jesse': https://www.youtube.com/watch?v=29ddZX4wjoE&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=224
      225. 'Building a Website: Team Page - Live Coding with Jesse': https://www.youtube.com/watch?v=pfgqJU1lG78&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=225
      226. 'Building a Website (P1D2) - Live Coding with Jesse': https://www.youtube.com/watch?v=rgYQ7nUulAQ&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=226
    """

    print("\n" + "-" * 100 + "\n")

    url_playlist = "https://www.youtube.com/playlist?list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG"
    items = search_youtube(url_playlist)
    __print_video_list(items)
    """
    Items (7):
        1. 'Intro to Java Programming - Course for Absolute Beginners': https://www.youtube.com/watch?v=GoXwIVyNvX0&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=1
        2. 'Functional Programming in Java - Full Course': https://www.youtube.com/watch?v=rPSL1alFIjI&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=2
        3. 'Spring Boot Tutorial for Beginners (Java Framework)': https://www.youtube.com/watch?v=vtPkZShrvXQ&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=3
        4. 'Learn Java 8 - Full Tutorial for Beginners': https://www.youtube.com/watch?v=grEKMHGYyns&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=4
        5. 'Data Structures Easy to Advanced Course - Full Tutorial from a Google Engineer': https://www.youtube.com/watch?v=RBSGKlAvoiM&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=5
        6. 'Spring Boot and Angular Tutorial - Build a Reddit Clone (Coding Project)': https://www.youtube.com/watch?v=DKlTBBuc32c&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=6
        7. 'Android Development for Beginners - Full Course': https://www.youtube.com/watch?v=fis26HvvDII&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=7
    """

    print("\n" + "-" * 100 + "\n")

    # Testing for: youtube, channel, channel videos
    print(len(get_video_list("https://www.youtube.com/")))
    print(len(get_video_list("https://www.youtube.com/c/TheBadComedian")))
    print(len(get_video_list("https://www.youtube.com/c/TheBadComedian/videos")))
    # 247
    # 45
    # 190

    print("\n" + "-" * 100 + "\n")

    is_live_now_video_list = [
        video
        for video in get_video_list("https://www.youtube.com/")
        if video.is_live_now
    ]
    print(f"Is live now ({len(is_live_now_video_list)}):")
    for i, video in enumerate(is_live_now_video_list, 1):
        print(f"{i}. {video.title!r}: {video.url}")

    print("\n" + "-" * 100 + "\n")

    items = search_youtube("щенки", maximum_items=25)
    __print_video_list(items)
    """
    Items (25):
        1. '🐾 Дружные мопсы - Серия 1 Сезон 1 - Мультфильмы Disney': https://www.youtube.com/watch?v=Eqyz-bFtkEM
        2. 'Лучшие Приколы про собак | Подборка приколов про собак и щенков #8': https://www.youtube.com/watch?v=wNqZM7e0_18
        3. 'СМЕШНЫЕ СОБАКИ И ЩЕНКИ 2020': https://www.youtube.com/watch?v=Grjk1K0YPSU
        ...
       23. 'Щенячий патруль и Мегащенки  Новые серии - 2021': https://www.youtube.com/watch?v=Gq63Zl0OL4k
       24. 'КАК ЩЕНКИ РАДУЮТСЯ МОЕМУ ПРИХОДУ АЛАБАЙ / КАК ЩЕНКИ АЛАБАЙ ЗАБАВНО БАЛУЮТСЯ': https://www.youtube.com/watch?v=QaMebbbCQ9E
       25. 'Макс и Катя играют с сюрпризами в огромных яйцах': https://www.youtube.com/watch?v=Mt7oS8Yq8YY
    """

    print("\n" + "-" * 100 + "\n")

    items = search_youtube(
        "https://www.youtube.com/results?search_query=slipknot official",
        maximum_items=50,
    )
    __print_video_list(items)
    """
    Items (50):
        1. 'Knotfest Los Angeles 2021: On-Sale Now': https://www.youtube.com/watch?v=8ueHLoI8htY
        2. 'Joey Jordison: 1975 - 2021': https://www.youtube.com/watch?v=5hejcY2p4A4
        3. 'Knotfest Los Angeles: November 5, 2021 [TRAILER]': https://www.youtube.com/watch?v=9qXnhQ0p7FA
        ...
       48. 'Slipknot: Live at Download Festival 2019': https://www.youtube.com/watch?v=QO3j9niG1Og
       49. 'Slipknot - Orphan (Audio)': https://www.youtube.com/watch?v=dvLp3XPNAZ0
       50. 'Slipknot - Spit It Out [OFFICIAL VIDEO]': https://www.youtube.com/watch?v=ZPUZwriSX4M
    """

    print("\n" + "-" * 100 + "\n")

    url = "https://www.youtube.com/playlist?list=PLZfhqd1-Hl3DtfKRjleAWB-zYJ-pj7apK"
    items = search_youtube_with_filter(url)
    print(f"Items ({len(items)}): {items}")
    # Items (3): ['История серии Diablo. Акт I', 'История серии Diablo. Акт II', 'История серии Diablo. Акт III']

    print("\n" + "-" * 100 + "\n")

    text = "Gorgeous Freeman -"
    url = "https://www.youtube.com/user/antoine35DeLak/search?query=" + text
    items = search_youtube_with_filter(url)
    print(f"Items ({len(items)}): {items}")
    # Items (46): ['Gorgeous Freeman - Episode 1 - The Suit', ..., 'The Epileptic Seizure [Gmod]']

    items = search_youtube_with_filter(url, filter_func=lambda name: text in name)
    print(f"Filtered items ({len(items)}): {items}")
    # Filtered items (3): ['Gorgeous Freeman - Episode 1 - The Suit', 'Gorgeous Freeman - Episode 3 - The Part 1', 'Gorgeous Freeman - Episode 2 - The Crowbar']

    print("\n" + "-" * 100 + "\n")

    text = "Sally Face"
    url = "https://www.youtube.com/user/HellYeahPlay/search?query=" + text
    items = search_youtube_with_filter(url)
    print(f"Items ({len(items)}): {items}")
    # Items (244): ['ТВОРЕНИЯ ВЕЛЬЗЕВУЛА - Sally Face [ЭПИЗОД 4] #9', ..., 'ЛЕСБИЙСКИЙ ТРЭШНЯК - Love Is Strange']

    items = search_youtube_with_filter(
        url, filter_func=lambda name: text in name and "эпизод" in name.lower()
    )
    print(f"Filtered items ({len(items)}): {items}")
    # Filtered items (14): ['ТВОРЕНИЯ ВЕЛЬЗЕВУЛА - Sally Face [ЭПИЗОД 4] #9', ..., 'ПОИСК МЕРТВЫХ ЛЮДЕЙ ☠️ Sally Face [ЭПИЗОД 2] #4']

    print("\n" + "-" * 100 + "\n")

    # Test for MIX
    try:
        url = "https://www.youtube.com/watch?v=QKEjrOIrCBI&list=RDQKEjrOIrCBI&start_radio=1"
        playlist = Playlist.get_from(url)
        print(playlist)
        print(len(playlist.video_list))
        __print_video_list(playlist.video_list)
    except AlertError as e:
        print(f"Error: {str(e)!r} for {url}")
    # Error: 'Этот тип плейлиста недоступен для просмотра.' for https://www.youtube.com/watch?v=QKEjrOIrCBI&list=RDQKEjrOIrCBI&start_radio=1
