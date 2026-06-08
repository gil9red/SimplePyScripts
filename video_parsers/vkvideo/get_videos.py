#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self, Generator

# NOTE: https://playwright.dev/python/docs/library#pip
#   pip install playwright==1.50.0
#   playwright install firefox
from playwright.sync_api import sync_playwright, Response

import requests

MAX_VIDEOS_SAFETY_LIMIT: int = 100


@dataclass(frozen=True)
class VideoInfo:
    id: int
    owner_id: int
    title: str
    direct_url: str | None
    share_url: str | None
    date: datetime
    description: str | None
    duration: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data["id"],
            owner_id=data["owner_id"],
            title=data["title"],
            direct_url=data.get("direct_url"),
            share_url=data.get("share_url"),
            date=datetime.fromtimestamp(data["date"]),
            description=data.get("description"),
            duration=data["duration"],
        )


@dataclass
class ApiInfo:
    url: str
    headers: dict[str, str]
    rq_data: dict[str, str]
    rs_data: dict[str, Any]


def get_api_info(url: str) -> ApiInfo:
    with sync_playwright() as p:
        browser = p.firefox.launch()

        page = browser.new_page()
        page.set_default_timeout(90_000)

        page.goto(url, wait_until="commit")

        def is_api(rs: Response) -> bool:
            url: str = rs.url
            return (
                "api" in url
                and rs.request.method == "POST"
                and rs.status == 200
                # NOTE: Уточнение с "?" в конце для исключения ссылки вида catalog.getVideoShowcase
                and ("/video.getFromAlbum?" in url or "/catalog.getVideo?" in url)
                and "json" in str(rs.headers)
            )

        with page.expect_response(is_api) as response_info:
            rs = response_info.value
            return ApiInfo(
                url=rs.url,
                headers=rs.request.headers,
                rq_data=rs.request.post_data_json,
                rs_data=rs.json(),
            )


def parse_videos(rs: dict[str, Any]) -> list[VideoInfo]:
    videos: list[dict[str, Any]]
    if "videos" in rs:  # На странице канала
        videos = rs["videos"]
    else:  # На странице плейлиста
        videos = [item["video"] for item in rs["items"]]

    return [VideoInfo.from_dict(video) for video in videos]


def paginate_by_offset(
    session: requests.Session,
    url: str,
    init_rq_data: dict[str, Any],
    _: dict[str, Any],
) -> Generator[list[VideoInfo], None, None]:
    """Генератор для постраничной пагинации (Альбомы)."""

    rq_data: dict[str, Any] = init_rq_data
    rq_data["offset"] = int(rq_data["offset"])
    rq_data["count"] = int(rq_data["count"])

    while True:
        rq_data["offset"] += rq_data["count"]

        rs = session.post(url, data=rq_data)
        rs.raise_for_status()

        rs_data = rs.json()["response"]

        videos = parse_videos(rs_data)
        if not videos:
            break

        yield videos


def paginate_by_token(
    session: requests.Session,
    url: str,
    init_rq_data: dict[str, Any],
    init_rs_data: dict[str, Any],
) -> Generator[list[VideoInfo], None, None]:
    """Генератор для курсорной пагинации (Каталог)."""

    section_id, next_from = None, None
    for section in init_rs_data["catalog"]["sections"]:
        if "next_from" in section:
            section_id, next_from = section["id"], section["next_from"]
            break

    # Первый запрос к catalog.getVideo, а последующие через catalog.getSection
    url = url.replace("/catalog.getVideo", "/catalog.getSection")
    rq_data: dict[str, Any] = {
        "section_id": section_id,
        "start_from": next_from,
        "access_token": init_rq_data["access_token"],
    }

    while True:
        if not rq_data.get("start_from"):
            break

        rs = session.post(url, data=rq_data)
        rs.raise_for_status()

        rs_data = rs.json()["response"]

        videos = parse_videos(rs_data)
        if not videos:
            break

        yield videos

        rq_data["start_from"] = rs_data.get("section", {}).get("next_from")


def get_videos(
    url: str,
    max_items: int | None = MAX_VIDEOS_SAFETY_LIMIT,
) -> list[VideoInfo]:
    # Вернется первая порция запросов
    api_info: ApiInfo = get_api_info(url)

    url: str = api_info.url

    if "/video.getFromAlbum" in url:
        pagination_provider = paginate_by_offset
    elif "/catalog.getVideo" in url:
        pagination_provider = paginate_by_token
    else:
        raise Exception("Неизвестный тип API")

    rs_data: dict[str, Any] = api_info.rs_data["response"]
    all_videos: list[VideoInfo] = parse_videos(rs_data)

    session = requests.Session()
    session.headers.update(api_info.headers)

    for chunk in pagination_provider(session, url, api_info.rq_data, rs_data):
        all_videos += chunk
        if max_items and len(all_videos) >= max_items:
            break

        time.sleep(1)

    return all_videos[:max_items] if max_items else all_videos


if __name__ == "__main__":

    def _print_videos(videos: list[VideoInfo]):
        print(f"Video ({len(videos)}):")

        width: int = len(str(len(videos)))

        for i, video in enumerate(videos, 1):
            print(f"    {i:>{width}}. {video}")

        assert videos != list(set(videos))

    # Пример из плейлиста (один запрос вернет 25 шт.)
    url: str = "https://vkvideo.ru/playlist/-1719791_48513772"

    print(url)
    videos: list[VideoInfo] = get_videos(url, max_items=50)
    _print_videos(videos)
    assert len(videos) == 50
    """
    Video (50):
         1. VideoInfo(id=456265497, owner_id=-1719791, title='Этих видео НЕ БЫЛО в +100500 🤐', direct_url='https://vkvideo.ru/video-1719791_456265497?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456265497?pl=-1719791_48513772', date=datetime.datetime(2026, 5, 30, 17, 24, 7), description='Эпизод # 556 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/6b52091c-d9a7-4395-a9c1-1390baf39f7b?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18972\n\n00:00 ПРЕДИСЛОВИЕ\n00:29 КЛАССИЧЕСКОЕ ИНТРО\n00:40 ЯЗЬ!\n04:05 НИКИТА ЛИТВИНКОВ\n08:13 НОРМАЛЬНО\n11:22 НАТАЛЬЯ МОРСКАЯ ПЕХОТА\n14:15 КЛАССИЧЕСКОЕ АУТРО\n\nПо вопросам рекламы: maks100500@didenokteam.com', duration=880)
         2. VideoInfo(id=456265161, owner_id=-1719791, title='Пора ЗАВЯЗЫВАТЬ \U0001fae9 / +100500', direct_url='https://vkvideo.ru/video-1719791_456265161?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456265161?pl=-1719791_48513772', date=datetime.datetime(2026, 4, 18, 16, 47, 4), description='Эпизод # 555 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/2d5df23d-9454-4679-8c12-a27955fddbc9?share=post_link \nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18884\n\n00:00 ПРИВЕТЛИВЫЙ ПАССАЖИР\n02:03 ИНТРО\n02:22 ЧЕЛОВЕК-РУЧНИК\n04:51 НЕВОЗМОЖНЫЙ УЗЕЛ\n07:43 МГНОВЕННАЯ ОБИДА\n09:59 МУЗЫКАЛЬНЫЙ КОНЕЦ\n\nПо вопросам рекламы: maks100500@didenokteam.com', duration=623)
         3. VideoInfo(id=456264517, owner_id=-1719791, title='ДАНИЛ КОЛБАСЕНКО / +100500', direct_url='https://vkvideo.ru/video-1719791_456264517?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456264517?pl=-1719791_48513772', date=datetime.datetime(2026, 3, 3, 21, 7, 41), description='Эпизод # 554 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/ad53a66d-54d3-43f9-80a2-41242cb7da8d?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18769\n\n00:00 ДАНИЛ КОЛБАСЕНКО\n02:55 ИНТРО\n03:13 ГОЛУБЯТНЯ В ДЕСЯТКЕ\n05:02 ПАРУСА ИЗ КАНАЛИЗАЦИИ\n07:03 АРОМАТНЫЕ ПАЛЬЧИКИ\n09:22 МУЗЫКАЛЬНЫЙ КОНЕЦ\n\nПо вопросам рекламы: maks100500@didenokteam.com', duration=599)
        ...
        48. VideoInfo(id=456258671, owner_id=-1719791, title='+100500 - ТОП КОНТЕНТ ИЗ TikTok', direct_url='https://vkvideo.ru/video-1719791_456258671?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456258671?pl=-1719791_48513772', date=datetime.datetime(2021, 8, 5, 15, 25, 38), description='Эпизод # 506 :D\nСЛУШАТЬ ПЕСНЮ 2ND SEASON - ДАБЛ ОРАНЖ 👉🏼 https://ffm.to/2ndxseason_doubleorange\nTelegram канал: https://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nInstagram +100500 с видосами и мемами: https://www.instagram.com/100500_vidowsov/\n100500_Play (Telegram канал с новостями из мира видеоигр): https://t.me/joinchat/AAAAAFgiJqyAY4vl5UiIaQ\nПаблик +100500 ВКонтакте: https://vk.com/maximplus100500\nMoran Days (Второй Канал) : http://www.youtube.com/user/MoranDays\nInstagram: http://instagram.com/adam_moran\nTwitter: http://twitter.com/maxplus100500\n\nВидео из эпизода: https://vk.com/wall-1719791_1809374\n\n0:00 ПРЕДИСЛОВИЕ\n0:54 ИНТРО\n1:20 СПАСИТЕЛЬНОЕ ПИВО\n3:52 АНГЛИЧАНИН ВЫРАСТИЛ БАНАНЫ\n4:54 ЗДРАВЫЙ ПАЦАН\n6:43 ОЛИМПИЙСКОЕ ПРЕДЛОЖЕНИЕ\n7:50 Я ПРЫГНУ\n9:58 ПЛАТНОЕ СПАСЕНИЕ НА ВОДЕ\n11:40 КОМПЬЮТЕРНАЯ БУХТА\n14:39 ПРОЩАЛОЧКА\n15:11 МУЗЫКАЛЬНЫЙ КОНЕЦ\n15:58 СЦЕНА ПОСЛЕ ТИТРОВ\n\nВидео для обзора: https://docs.google.com/forms/d/1gx6iUl5Z', duration=994)
        49. VideoInfo(id=456258038, owner_id=-1719791, title='+100500 - ПИВО С ПРОДОЛЖЕНИЕМ 😏', direct_url='https://vkvideo.ru/video-1719791_456258038?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456258038?pl=-1719791_48513772', date=datetime.datetime(2021, 6, 23, 19, 27, 37), description='Эпизод # 505 :D\nСЛУШАТЬ ПЕСНЮ 2ND SEASON - ДАБЛ ОРАНЖ 👉🏼 https://ffm.to/2ndxseason_doubleorange\nTelegram канал: https://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nInstagram +100500 с видосами и мемами: https://www.instagram.com/100500_vidowsov/\n100500_Play (Telegram канал с новостями из мира видеоигр): https://t.me/joinchat/AAAAAFgiJqyAY4vl5UiIaQ\nПаблик +100500 ВКонтакте: https://vk.com/maximplus100500\nMoran Days (Второй Канал) : http://www.youtube.com/user/MoranDays\nInstagram: http://instagram.com/adam_moran\nTwitter: http://twitter.com/maxplus100500\n\nВидео из эпизода: https://vk.com/wall-1719791_1789398\n\n0:00 ИНТРО\n0:27 ЧЕСНОК ХОЧЕШЬ\n2:41 ПОТЕРЯЛ ПОДОШВУ\n4:01 ФУТБОЛЬНЫЙ ПАРАШЮТИСТ\n5:27 ПИВО С ПРОДОЛЖЕНИЕМ\n7:15 ПРОЩАЛОЧКА\n7:51 МУЗЫКАЛЬНЫЙ КОНЕЦ\n8:10 СЦЕНА ПОСЛЕ ТИТРОВ\n\nВидео для обзора: https://docs.google.com/forms/d/1gx6iUl5ZvEyI_01TvGZT97qAMx-4Uum6zOGM02nIvrE/viewform?usp=send_form\n\n#ПИВОСПРОДОЛЖЕНИЕМ', duration=577)
        50. VideoInfo(id=456257788, owner_id=-1719791, title='+100500 - ЖЁСТКАЯ РЫБАЛКА С МОТЕЙ', direct_url='https://vkvideo.ru/video-1719791_456257788?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456257788?pl=-1719791_48513772', date=datetime.datetime(2021, 6, 10, 22, 3, 19), description='Эпизод # 504 :D\nСЛУШАТЬ ПЕСНЮ 2ND SEASON - ДАБЛ ОРАНЖ 👉🏼 https://ffm.to/2ndxseason_doubleorange\nTelegram канал: https://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nInstagram +100500 с видосами и мемами: https://www.instagram.com/100500_vidowsov/\n100500_Play (Telegram канал с новостями из мира видеоигр): https://t.me/joinchat/AAAAAFgiJqyAY4vl5UiIaQ\nПаблик +100500 ВКонтакте: https://vk.com/maximplus100500\nMoran Days (Второй Канал) : http://www.youtube.com/user/MoranDays\nInstagram: http://instagram.com/adam_moran\nTwitter: http://twitter.com/maxplus100500\n\nВидео из эпизода: \n\n0:00 ИНТРО\n0:27 ЗА ВИАГРОЙ В ЛОМБАРД\n2:42 ЧАЙКА-ПАССАЖИР\n4:12 МОТЯ\n6:27 КАРТОФЕЛЬНЫЙ ЛАЙФХАК\n8:27 ПРОЩАЛОЧКА\n9:53 МУЗЫКАЛЬНЫЙ КОНЕЦ\n9:19 СЦЕНА ПОСЛЕ ТИТРОВ\n\nВидео для обзора: https://docs.google.com/forms/d/1gx6iUl5ZvEyI_01TvGZT97qAMx-4Uum6zOGM02nIvrE/viewform?usp=send_form\n\n#МОТЯ #РЫБАЛКА', duration=605)
    """

    print()

    print(url)
    videos: list[VideoInfo] = get_videos(url, max_items=9999)
    _print_videos(videos)
    assert len(videos) > 100
    """
    Video (122):
          1. VideoInfo(id=456265497, owner_id=-1719791, title='Этих видео НЕ БЫЛО в +100500 🤐', direct_url='https://vkvideo.ru/video-1719791_456265497?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456265497?pl=-1719791_48513772', date=datetime.datetime(2026, 5, 30, 17, 24, 7), description='Эпизод # 556 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/6b52091c-d9a7-4395-a9c1-1390baf39f7b?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18972\n\n00:00 ПРЕДИСЛОВИЕ\n00:29 КЛАССИЧЕСКОЕ ИНТРО\n00:40 ЯЗЬ!\n04:05 НИКИТА ЛИТВИНКОВ\n08:13 НОРМАЛЬНО\n11:22 НАТАЛЬЯ МОРСКАЯ ПЕХОТА\n14:15 КЛАССИЧЕСКОЕ АУТРО\n\nПо вопросам рекламы: maks100500@didenokteam.com', duration=880)
          2. VideoInfo(id=456265161, owner_id=-1719791, title='Пора ЗАВЯЗЫВАТЬ \U0001fae9 / +100500', direct_url='https://vkvideo.ru/video-1719791_456265161?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456265161?pl=-1719791_48513772', date=datetime.datetime(2026, 4, 18, 16, 47, 4), description='Эпизод # 555 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/2d5df23d-9454-4679-8c12-a27955fddbc9?share=post_link \nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18884\n\n00:00 ПРИВЕТЛИВЫЙ ПАССАЖИР\n02:03 ИНТРО\n02:22 ЧЕЛОВЕК-РУЧНИК\n04:51 НЕВОЗМОЖНЫЙ УЗЕЛ\n07:43 МГНОВЕННАЯ ОБИДА\n09:59 МУЗЫКАЛЬНЫЙ КОНЕЦ\n\nПо вопросам рекламы: maks100500@didenokteam.com', duration=623)
          3. VideoInfo(id=456264517, owner_id=-1719791, title='ДАНИЛ КОЛБАСЕНКО / +100500', direct_url='https://vkvideo.ru/video-1719791_456264517?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456264517?pl=-1719791_48513772', date=datetime.datetime(2026, 3, 3, 21, 7, 41), description='Эпизод # 554 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/ad53a66d-54d3-43f9-80a2-41242cb7da8d?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18769\n\n00:00 ДАНИЛ КОЛБАСЕНКО\n02:55 ИНТРО\n03:13 ГОЛУБЯТНЯ В ДЕСЯТКЕ\n05:02 ПАРУСА ИЗ КАНАЛИЗАЦИИ\n07:03 АРОМАТНЫЕ ПАЛЬЧИКИ\n09:22 МУЗЫКАЛЬНЫЙ КОНЕЦ\n\nПо вопросам рекламы: maks100500@didenokteam.com', duration=599)
        ...
        120. VideoInfo(id=456240348, owner_id=-1719791, title='+100500 - Порнография На Переезде', direct_url='https://vkvideo.ru/video-1719791_456240348?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456240348?pl=-1719791_48513772', date=datetime.datetime(2019, 9, 9, 21, 31, 39), description='Эпизод #435 :D\nПаблик +100500 ВКонтакте: https://vk.com/maximplus100500\nTelegram канал: https://tg.telepult.pro/vidowsov_100500\n\nMoran Days (Второй...', duration=750)
        121. VideoInfo(id=456240213, owner_id=-1719791, title='+100500 - Поцеловал Верблюда Сзади', direct_url='https://vkvideo.ru/video-1719791_456240213?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456240213?pl=-1719791_48513772', date=datetime.datetime(2019, 8, 30, 20, 49, 58), description='Эпизод #434 :D\nHONOR 20 PRO с подарками при покупке на официальном сайте: https://clck.ru/HpYMA\n\nMoran Days (Второй Канал) : http://www.youtube.com...', duration=732)
        122. VideoInfo(id=456239908, owner_id=-1719791, title='+100500 - НАШЕСТВИЕ 2019', direct_url='https://vkvideo.ru/video-1719791_456239908?pl=-1719791_48513772', share_url='https://vkvideo.ru/video-1719791_456239908?pl=-1719791_48513772', date=datetime.datetime(2019, 8, 5, 18, 22, 42), description='Эпизод #433 :D\nMoran Days (Второй Канал) : http://www.youtube.com/user/MoranDays\n\nInstagram: http://instagram.com/adam_moran\n\nTwitter: http://twitt...', duration=599)
    """

    print()

    # Пример из канала (один запрос вернет 20 шт.)
    url = "https://vkvideo.ru/@public_redcynic/all"

    print(url)
    videos: list[VideoInfo] = get_videos(url, max_items=50)
    _print_videos(videos)
    assert len(videos) == 50
    """
    Video (50):
         1. VideoInfo(id=456243328, owner_id=-58569409, title='«Хищник: Дикие земли». Обзор «Красного Циника» UNCUT', direct_url=None, share_url='https://vkvideo.ru/video-58569409_456243328', date=datetime.datetime(2026, 3, 25, 17, 26, 14), description=None, duration=0)
         2. VideoInfo(id=456243326, owner_id=-58569409, title='«Хищник: Дикие земли». Обзор «Красного Циника»', direct_url='https://vkvideo.ru/video-58569409_456243326', share_url='https://vkvideo.ru/video-58569409_456243326', date=datetime.datetime(2026, 3, 24, 17, 0, 38), description='https://boosty.to/redcynic – аккаунт на Бусти\nhttps://vk.com/public_redcynic – группа «В контакте»\nКошелёк Ю.Money: 410011854513048\nhttps://t.me/redcynic – канал в Телеграме\n\nhttp://www.donationalerts.ru/r/redcynic – взнос на Донейшн Алертс\nhttps://www.patreon.com/bePatron?u=5206451 – страница на Патреоне\nhttps://www.youtube.com/RedCynicRus/join – стать Спонсором канала\nhttp://redcynic.com – мой сайт\n\nДэн Трахтенберг, конечно, разошёлся по полной, за четыре года наваяв больше киношек про Хищнегов, чем было заснято за предыдущие восемнадцать лет. И в этот раз он замахнулся на сложнейшее, пообещав показать внутренний быт и культуру самих инопланетных охотников от их же лица... То есть уже на самом старте извратив саму суть изначальных картин. Когда же ещё и заявили про комедийные буга-гашечки в основе сюжета, стало ясно, что нас ожидает привычное от Трахтенберга. Очередная смесь бреда, идиотии и издевательств над культовой франшизой. Как в воду глядели… Но давайте-таки подробно разберём, что для него Хищники есть...', duration=3760)
         3. VideoInfo(id=456243317, owner_id=-58569409, title='«Одни из нас». Второй сезон. Обзор «Красного Циника» UNCUT', direct_url=None, share_url='https://vkvideo.ru/video-58569409_456243317', date=datetime.datetime(2026, 1, 4, 23, 19, 5), description=None, duration=0)
       
        ...
        48. VideoInfo(id=456242283, owner_id=-58569409, title='Вступление к  Red Alert 2', direct_url='https://vkvideo.ru/video-58569409_456242283', share_url='https://vkvideo.ru/video-58569409_456242283', date=datetime.datetime(2021, 10, 27, 17, 51, 17), description='Red Alert 2 Intro — Озвучка City — AI Upscale 60 FPS by RC', duration=238)
        49. VideoInfo(id=456242254, owner_id=-58569409, title='«Власть огня». Обзор «Красного Циника»', direct_url='https://vkvideo.ru/video-58569409_456242254', share_url='https://vkvideo.ru/video-58569409_456242254', date=datetime.datetime(2021, 10, 11, 22, 6, 49), description='', duration=1564)
        50. VideoInfo(id=456242209, owner_id=-58569409, title='«Армия мертвецов». Обзор «Красного Циника»', direct_url='https://vkvideo.ru/video-58569409_456242209', share_url='https://vkvideo.ru/video-58569409_456242209', date=datetime.datetime(2021, 9, 4, 22, 59, 55), description='https://www.patreon.com/bePatron?u=5206451 – страница на Патреоне\nhttps://boosty.to/redcynic – аккаунт на Бусти\nhttps://www.youtube.com/RedCynicRus/join – стать Спонсором канала\nhttp://www.donationalerts.ru/r/redcynic – взнос на Донейшн Алертс\nhttp://redcynic.com – мой сайт\nhttps://vk.com/public_redcynic – группа «В контакте»\nhttps://twitter.com/RedCynicRus – мой Твиттер\nhttps://www.facebook.com/red.cynic – Фэйсбук\nhttps://www.instagram.com/red_cynic_rc – мой Инстаграм\n\nНе откладывая дело в долгий ящик, давайте взглянем на следующее, после «Лиги Справедливости», кино Зака Снайдера, дабы оценить все грани таланта сумрачного гения. И тем интереснее будет этот процесс, если знать, что в своё время именно с фильма про зомби мэтр начал свою карьеру. Фильм, в общем-то знаковый для всего жанра. Такого же уровня ждали сейчас. Тем более учитывая шумиху, которая поднялась вокруг создания картины. И тот факт, что Зак Снайдер лелеял замысел её снять начиная аж с 2007 года, а может быть и ран', duration=3562)
    """

    print()

    print(url)
    videos: list[VideoInfo] = get_videos(url, max_items=9999)
    _print_videos(videos)
    assert len(videos) > 100
    """
    Video (157):
          1. VideoInfo(id=456243328, owner_id=-58569409, title='«Хищник: Дикие земли». Обзор «Красного Циника» UNCUT', direct_url=None, share_url='https://vkvideo.ru/video-58569409_456243328', date=datetime.datetime(2026, 3, 25, 17, 26, 14), description=None, duration=0)
          2. VideoInfo(id=456243326, owner_id=-58569409, title='«Хищник: Дикие земли». Обзор «Красного Циника»', direct_url='https://vkvideo.ru/video-58569409_456243326', share_url='https://vkvideo.ru/video-58569409_456243326', date=datetime.datetime(2026, 3, 24, 17, 0, 38), description='https://boosty.to/redcynic – аккаунт на Бусти\nhttps://vk.com/public_redcynic – группа «В контакте»\nКошелёк Ю.Money: 410011854513048\nhttps://t.me/redcynic – канал в Телеграме\n\nhttp://www.donationalerts.ru/r/redcynic – взнос на Донейшн Алертс\nhttps://www.patreon.com/bePatron?u=5206451 – страница на Патреоне\nhttps://www.youtube.com/RedCynicRus/join – стать Спонсором канала\nhttp://redcynic.com – мой сайт\n\nДэн Трахтенберг, конечно, разошёлся по полной, за четыре года наваяв больше киношек про Хищнегов, чем было заснято за предыдущие восемнадцать лет. И в этот раз он замахнулся на сложнейшее, пообещав показать внутренний быт и культуру самих инопланетных охотников от их же лица... То есть уже на самом старте извратив саму суть изначальных картин. Когда же ещё и заявили про комедийные буга-гашечки в основе сюжета, стало ясно, что нас ожидает привычное от Трахтенберга. Очередная смесь бреда, идиотии и издевательств над культовой франшизой. Как в воду глядели… Но давайте-таки подробно разберём, что для него Хищники есть...', duration=3760)
          3. VideoInfo(id=456243317, owner_id=-58569409, title='«Одни из нас». Второй сезон. Обзор «Красного Циника» UNCUT', direct_url=None, share_url='https://vkvideo.ru/video-58569409_456243317', date=datetime.datetime(2026, 1, 4, 23, 19, 5), description=None, duration=0)
        ...
        155. VideoInfo(id=166665571, owner_id=-58569409, title='«Игра престолов» - Сезон 1. Рецензия «Красного Циника»', direct_url='https://vkvideo.ru/video-58569409_166665571', share_url='https://vkvideo.ru/video-58569409_166665571', date=datetime.datetime(2013, 11, 1, 2, 42, 58), description='www.redcynic.com http://vk.com/redcynic\n\nВ 2011 году на телевизионные экраны вышел сериал, который произвел огромный фурор. Шоу заслуженно получило признание как зрителей, так и критиков. В принципе, такой же теплый прием получил в своё время и первоисточник - роман под одноименным названием, чьим автором является Джордж Мартин.\n\nНо так ли на самом деле хорош роман? Так ли безупречен сериал? Данная рецензия - это сравнение сериала, романа и... здравого смысла.<br/><br/>', duration=1608)
        156. VideoInfo(id=166305114, owner_id=-58569409, title='«Красный рассвет». Обзор «Красного Циника»', direct_url='https://vkvideo.ru/video-58569409_166305114', share_url='https://vkvideo.ru/video-58569409_166305114', date=datetime.datetime(2013, 9, 19, 0, 11, 25), description='группа в ВК - http://vk.com/redcynic\nпаблик в ВК - http://vk.com/public_redcynic \nсайт - www.redcynic.com \n\nКто такие красные орки? Откуда они берутся? Об этом вам расскажет Джон Милиус! Уж кто-кто, а он так точно разбирается во всех оттенках красно-буро-малинового! Давайте же рассмотрим один из самых примечательных продуктов холодной войны. А потом поставим диагноз и Милиусу, и его оркам.', duration=2041)
        157. VideoInfo(id=166305092, owner_id=-58569409, title='«Война Богов: Бессмертные». Обзор «Красного Циника»', direct_url='https://vkvideo.ru/video-58569409_166305092', share_url='https://vkvideo.ru/video-58569409_166305092', date=datetime.datetime(2013, 9, 19, 0, 9, 9), description='группа в ВК - http://vk.com/redcynic\nпаблик в ВК - http://vk.com/public_redcynic \nсайт - www.redcynic.com \n\nЧто получится, если режиссёру индийского происхождения поручить экранизацию древнегреческих легенд? Как Тарсем Синх подошёл к созданию своих «Бессмертных»? Какая муза куса... посещала его во время творческого процесса? А давайте это прямо сейчас и узнаем ...', duration=2166)
    """
