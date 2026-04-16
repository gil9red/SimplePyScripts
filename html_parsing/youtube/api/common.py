#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re
import time

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Generator
from urllib.parse import urljoin, urlparse, parse_qs

# pip install dpath==2.0.5
import dpath.util

# pip install requests==2.32.2
import requests

# pip install tzlocal==4.1
import tzlocal


class AlertError(Exception):
    pass


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
)
BASE_URL = "https://www.youtube.com"


session = requests.Session()
session.headers["User-Agent"] = USER_AGENT

# NOTE: Accept all (required for mixes)
# SOURCE: https://github.com/yt-dlp/yt-dlp/blob/ed24640943872c4cf30d7cc4601bec87b50ba03c/yt_dlp/extractor/youtube/_base.py#L614
session.cookies["SOCS"] = "CAI"


def process_text(text: str) -> str:
    return text.strip().replace("\xa0", " ").replace("\u202f", " ")


def parse_date(value: str) -> date | None:
    for regex_pattern, months in [
        (
            r"(?P<month>%s) (?P<day>\d{,2}), (?P<year>\d{4})",
            ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'july', 'aug', 'sep', 'oct', 'nov', 'dec'],
        ),
        (
            r"(?P<day>\d{,2}) (?P<month>%s)\.? (?P<year>\d{4})",
            ['янв', 'февр', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сент', 'окт', 'нояб', 'дек'],
        ),
    ]:
        regex = regex_pattern % "|".join(months)
        m = re.search(regex, value, flags=re.IGNORECASE)
        if not m:
            continue

        return date(
            year=int(m["year"]),
            month=months.index(m["month"]) + 1,
            day=int(m["day"]),
        )

    return


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


def download_url_as_bytes(url: str) -> bytes:
    rs = session.get(url)
    rs.raise_for_status()
    return rs.content


def get_yt_cfg_data(html: str) -> dict:
    m = re.search(r"ytcfg\.set\((\{.+?\})\);", html)
    if not m:
        raise Exception("Не удалось найти на странице ytcfg.set!")

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


def dict_merge(d1: dict, d2: dict) -> None:
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):
            dict_merge(d1[k], v)
        else:
            d1[k] = v


def get_yt_initial_data(html: str) -> dict | None:
    patterns = [
        re.compile(r'window\["ytInitialData"\] = (\{.+?\});'),
        re.compile(r"var ytInitialData = (\{.+?\});"),
    ]

    for pattern in patterns:
        m = pattern.search(html)
        if m:
            data_str = m.group(1)
            return json.loads(data_str)


def load(url: str) -> tuple[requests.Response, dict]:
    rs = session.get(url)
    rs.raise_for_status()

    data = get_yt_initial_data(rs.text)
    if not data:
        raise Exception("Could not find ytInitialData!")

    raise_if_error(data)

    return rs, data


def get_yt_initial_player_response(html: str) -> dict:
    m = re.search(r"ytInitialPlayerResponse = (\{.+?\});", html)
    if not m:
        raise Exception("Не удалось найти на странице ytInitialPlayerResponse!")

    return json.loads(m.group(1))


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


def get_context_with_continuation(
    url: str,
    yt_cfg_data: dict,
    continuation_item: dict,
) -> dict:
    innertube_context = yt_cfg_data.get("INNERTUBE_CONTEXT")
    if not innertube_context:
        raise Exception("Значение INNERTUBE_CONTEXT должно быть задано в yt_cfg_data!")

    continuation_endpoint: dict = continuation_item["continuationEndpoint"]
    click_tracking_params: str = continuation_endpoint["clickTrackingParams"]
    continuation_token: str = dpath.util.get(
        continuation_endpoint,
        glob="**/continuationCommand/token",
    )

    pattern_next_page_data = get_context_data(url, innertube_context)
    pattern_next_page_data["continuation"] = continuation_token
    pattern_next_page_data["context"]["clickTracking"] = {
        "clickTrackingParams": click_tracking_params,
    }

    return pattern_next_page_data


def get_api_url_from_continuation_item(url: str, continuation_item: dict) -> str:
    api_url = dpath.util.get(continuation_item, "**/webCommandMetadata/apiUrl")
    return urljoin(url, api_url)


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
    yt_initial_data: dict,
    rs: requests.Response,
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
            # Может вернуться несколько continuationItemRenderer, берем первый
            continuation_item = dpath.util.values(data, "**/continuationItemRenderer")[0]
        except (KeyError, IndexError):
            break

        url_next_page_data = get_api_url_from_continuation_item(
            rs.url, continuation_item
        )

        next_page_data = get_context_with_continuation(
            rs.url, yt_cfg_data, continuation_item
        )
        rs = session.post(
            url_next_page_data,
            params={"key": innertube_api_key},
            json=next_page_data,
        )
        data = rs.json()

        yield from get_raw_video_renderer_items(data)


@dataclass
class Context:
    data_video: dict | None = None
    yt_initial_data: dict | None = None
    yt_cfg_data: dict | None = None
    rs: requests.Response | None = None


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
    duration_seconds: int | None = None
    duration_text: str | None = None
    seq: int | None = None
    is_live_now: bool = False
    thumbnails: list[Thumbnail] = field(default_factory=list, repr=False, compare=False)
    view_count: int | None = None
    create_date: date | None = None
    create_date_raw: str | None = None
    is_lasy: bool = True
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
        parent_context: Context | None = None,
        url_video: str = "",
    ) -> "Video":
        if parent_context and parent_context.yt_initial_data:
            raise_if_error(parent_context.yt_initial_data)

        title = cls.parse_title(data_video)

        if not url_video:
            url_video = cls.parse_url(data_video)

        duration_seconds = cls.parse_duration_seconds(data_video)
        if duration_seconds:
            duration_text = seconds_to_str(duration_seconds)
        else:
            duration_text = None

        try:
            seq = int(data_video["index"]["simpleText"])
        except:
            seq = None

        try:
            create_date_raw: str | None = process_text(
                data_video["dateText"]["simpleText"]
            )
        except:
            create_date_raw = None

        try:
            create_date: date | None = parse_date(create_date_raw)
        except:
            create_date = None

        thumbnails = [
            Thumbnail.get_from(thumbnail)
            for thumbnail in dpath.util.values(data_video, "thumbnail/thumbnails/*")
        ]

        try:
            view_count = int(data_video["viewCount"])
        except:
            view_count = None

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
            view_count=view_count,
            create_date=create_date,
            create_date_raw=create_date_raw,
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

        video = cls.parse_from(
            data_video=data_video,
            parent_context=context,
            url_video=url,
        )
        video.is_lasy = False

        return video

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
    duration_seconds: int | None = None
    duration_text: str | None = None
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

            # Extracting playlist id from url video
            if "/playlist?" not in url:
                url = cls.get_url(playlist_id)

        else:
            playlist_id = url_or_id
            url = cls.get_url(playlist_id)

        rs, yt_initial_data = load(url)

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
