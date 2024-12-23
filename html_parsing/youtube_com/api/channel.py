#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, field
from urllib.parse import urlparse, parse_qsl

# pip install dpath
import dpath.util

from .common import (
    session,
    load,
    get_yt_cfg_data,
    get_context_with_continuation,
    get_api_url_from_continuation_item,
)


def process_text(text: str) -> str:
    return text.strip().replace("\xa0", " ").replace("\u202f", " ")


def get_original_url(url: str) -> str:
    p = urlparse(url)
    if p.path != "/redirect" or not p.query:
        return url

    params = dict(parse_qsl(p.query))
    return params["q"]


@dataclass
class Link:
    title: str
    url: str

    @classmethod
    def parse_from(cls, data: dict) -> "Link":
        title = dpath.util.get(data, "title/content")

        url = dpath.util.get(data, "link/commandRuns/0/**/webCommandMetadata/url")
        url = get_original_url(url)

        return cls(
            title=process_text(title),
            url=url,
        )


@dataclass
class ChannelInfo:
    channel_id: str
    canonical_channel_url: str
    description: str
    subscriber_count_text: str
    view_count_text: str
    joined_date_text: str
    links: list[Link] = field(default_factory=list)

    @classmethod
    def parse_from(cls, data: dict) -> "ChannelInfo":
        return cls(
            channel_id=data["channelId"],
            canonical_channel_url=data["canonicalChannelUrl"],
            description=process_text(data["description"]),
            subscriber_count_text=process_text(data["subscriberCountText"]),
            view_count_text=process_text(data["videoCountText"]),
            joined_date_text=process_text(
                dpath.util.get(data, "joinedDateText/content")
            ),
            links=[
                Link.parse_from(item["channelExternalLinkViewModel"])
                for item in data.get("links", [])
            ],
        )


def get_channel_info(url: str) -> ChannelInfo:
    rs, yt_initial_data = load(url)

    yt_cfg_data: dict = get_yt_cfg_data(rs.text)

    # Действие на странице в профиле, открывающее "О канале"
    description_data: dict = dpath.util.get(
        yt_initial_data, "header/**/descriptionPreviewViewModel"
    )
    description_on_tap_data: dict = dpath.util.get(description_data, "**/onTap")
    continuation_item: dict = dpath.util.get(
        description_on_tap_data, "**/continuationItemRenderer"
    )

    context: dict = get_context_with_continuation(
        rs.url, yt_cfg_data, continuation_item
    )

    url_browse: str = get_api_url_from_continuation_item(rs.url, continuation_item)

    rs = session.post(url_browse, json=context, params={"prettyPrint": "false"})
    rs.raise_for_status()

    rs_data = rs.json()

    about_channel_data: dict = dpath.util.get(rs_data, "**/aboutChannelViewModel")
    return ChannelInfo.parse_from(about_channel_data)
