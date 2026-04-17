#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

# NOTE: https://playwright.dev/python/docs/library#pip
#   pip install playwright==1.50.0
#   playwright install firefox
from playwright.sync_api import sync_playwright, Response


@dataclass
class VideoInfo:
    id: int
    owner_id: int
    title: str
    direct_url: str
    date: datetime
    description: str
    duration: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data["id"],
            owner_id=data["owner_id"],
            title=data["title"],
            direct_url=data["direct_url"],
            date=datetime.fromtimestamp(data["date"]),
            description=data["description"],
            duration=data["duration"],
        )


def get_first_videos_raw(url: str) -> dict[str, Any]:
    with sync_playwright() as p:
        browser = p.firefox.launch()

        page = browser.new_page()
        page.set_default_timeout(90_000)

        page.goto(url, wait_until="commit")

        def is_api(rs: Response) -> bool:
            url: str = rs.url
            return (
                "api" in url
                and ("/video.getFromAlbum?" in url or "/catalog.getVideo?" in url)
                and rs.status == 200
            )

        with page.expect_response(is_api) as response_info:
            return response_info.value.json()


def get_first_videos(url: str) -> list[VideoInfo]:
    rs: dict[str, Any] = get_first_videos_raw(url)["response"]

    videos: list[dict[str, Any]]
    if "videos" in rs:  # На странице канала
        videos = rs["videos"]
    else:  # На странице плейлиста
        videos = [item["video"] for item in rs["items"]]

    return [VideoInfo.from_dict(video) for video in videos]


if __name__ == "__main__":

    def _print_videos(videos: list[VideoInfo]):
        print(f"Video ({len(videos)}):")
        print(*videos[:5], sep="\n")
        print("...")
        print(*videos[-5:], sep="\n")

    videos: list[VideoInfo] = get_first_videos(
        "https://vkvideo.ru/playlist/-1719791_48513772"
    )
    _print_videos(videos)
    """
    Video (25):
    VideoInfo(id=456264517, owner_id=-1719791, title='ДАНИЛ КОЛБАСЕНКО / +100500', direct_url='https://vkvideo.ru/video-1719791_456264517?pl=-1719791_48513772', date=datetime.datetime(2026, 3, 3, 21, 7, 41), description='Эпизод # 554 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/ad53a66d-54d3-43f9-80a2-41242cb7da8d?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18769\n\n00:00 ДАНИЛ КОЛБАСЕНКО\n02:55 ИНТРО\n03:13 ГОЛУБЯТНЯ В ДЕСЯТКЕ\n05:02 ПАРУСА ИЗ КАНАЛИЗАЦИИ\n07:03 АРОМАТНЫЕ ПАЛЬЧИКИ\n09:22 МУЗЫКАЛЬНЫЙ КОНЕЦ\n\nПо вопросам рекламы: maks100500@didenokteam.com', duration=599)
    VideoInfo(id=456264454, owner_id=-1719791, title='Чилловый козёл, который НА ЧИЛЛЕ 💤🐐 / +100500', direct_url='https://vkvideo.ru/video-1719791_456264454?pl=-1719791_48513772', date=datetime.datetime(2026, 2, 2, 20, 48, 34), description='Эпизод # 553 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/2ae907c7-1183-475e-824c-7959a0de3030?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18693\n\n00:00 ДРУГ В ОТРАЖЕНИИ\n01:46 ИНТРО\n02:04 ХЛОПУШКА ОТ МУХ\n03:41 ЧИЛЛОВЫЙ КОЗЁЛ\n05:19 ОСВЕЖИТЕЛЬ С ДУШКОМ\n07:22 МУЗЫКАЛЬНЫЙ КОНЕЦ', duration=473)
    VideoInfo(id=456264437, owner_id=-1719791, title='ОБЛЕЗЛЫЙ НОВЫЙ ГОД 🎄 Ёлка-Ёршик и Розетки На Ковре', direct_url='https://vkvideo.ru/video-1719791_456264437?pl=-1719791_48513772', date=datetime.datetime(2025, 12, 31, 20, 22, 31), description='Эпизод # 552 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/f81d5f16-a3ea-4aac-8fc2-aacff72fb645?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18571\n\n00:00 НОВОГОДНИЙ ЁРШИК\n02:04 ИНТРО\n02:23 ДЕД МОРОЗ ПОЛОЖИЛ\n03:48 ОЛИВЬЕШНЫЙ ГРИНЧ\n05:23 КРЕАТИВНЫЙ ЭЛЕКТРИК\n07:48 ПОЗДРАВЛЕНИЕ\n08:49 МУЗЫКАЛЬНЫЙ КОНЕЦ', duration=554)
    VideoInfo(id=456264423, owner_id=-1719791, title='ПАРКУР В КАБЛУКАХ 👠 / +100500', direct_url='https://vkvideo.ru/video-1719791_456264423?pl=-1719791_48513772', date=datetime.datetime(2025, 12, 19, 21, 14, 31), description='Эпизод # 551 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/cd2315b4-e05d-431d-96f1-52d126df8a34?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18516\n\n00:00 99 ПРОБЛЕМ\n02:19 ИНТРО\n02:38 АЛЬПИНИСТКА НА ШПИЛЬКАХ\n05:31 Я ВОТ СЮДА ЛЕЧУ\n07:09 ПЕРДОКОНЬ\n09:04 МУЗЫКАЛЬНЫЙ КОНЕЦ\n\nПо вопросам рекламы: 100500@hypeagency.ru', duration=574)
    VideoInfo(id=456264404, owner_id=-1719791, title='ПИТЕРСКИЙ ПРОГНОЗ ПОГОДЫ 🌧️ / +100500', direct_url='https://vkvideo.ru/video-1719791_456264404?pl=-1719791_48513772', date=datetime.datetime(2025, 12, 6, 18, 58, 53), description='Эпизод # 550 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/8443440f-42d0-4617-9218-d2a35c4e7441?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18470\n\n00:00 ОПОХМЕЛ ДЛЯ НЕЗНАКОМЦА\n02:17 ИНТРО\n02:36 ПИТЕРСКИЙ ПРОГНОЗ\n06:02 ПОДУШКА ЧЕШЕТСЯ\n07:35 РЮКЗАЧОК С СЮРПРИЗОМ\n09:51 МУЗЫКАЛЬНЫЙ КОНЕЦ\n\nПо вопросам рекламы: 100500@hypeagency.ru', duration=628)
    ...
    VideoInfo(id=456263435, owner_id=-1719791, title='РЫБА 🐟 КОТЛЕТЫ 🥩 КОНФЕТЫ 🍬 / +100500', direct_url='https://vkvideo.ru/video-1719791_456263435?pl=-1719791_48513772', date=datetime.datetime(2024, 2, 6, 1, 56, 30), description='Эпизод # 535 :D\nMORAN PLAYS (стримы)\nYOUTUBE: https://www.youtube.com/@MoranPlaysGames\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/MORANPLAYS\n\nTikTok: https://www.tiktok.com/@maxim_golopolosov\nTelegram канал: https://t.me/vidowsov100500\nПаблик +100500 ВКонтакте: https://vk.com/maximplus100500\nMoran Days (Второй Канал) : http://www.youtube.com/user/MoranDays\nTwitter: http://twitter.com/maxplus100500\n\nВидео из эпизода: https://vk.com/wall-1719791_1911322\n\n0:00 ПОДЗЕМНЫЙ СПОРТСМЕН\n1:10 ИНТРО \n1:27 РАЗРЕЗ ПРАВ\n3:06 БОЕВОЕ РАЗВЁРТЫВАНИЕ\n5:10 ПРОТИВОУГОННАЯ ЛАМПОЧКА\n6:59 РЫБА, КОТЛЕТЫ, КОНФЕТЫ\n9:00 МУЗЫКАЛЬНЫЙ КОНЕЦ', duration=570)
    VideoInfo(id=456263121, owner_id=-1719791, title='ИГРУШКИ ДЬЯВОЛА 😈 / +100500', direct_url='https://vkvideo.ru/video-1719791_456263121?pl=-1719791_48513772', date=datetime.datetime(2023, 9, 30, 3, 36, 39), description='Эпизод # 534 :D\nMORAN PLAYS (стримы)\nYOUTUBE: https://www.youtube.com/@MoranPlaysGames\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/MORANPLAYS\n\nTikTok: https://www.tiktok.com/@maxim_golopolosov\nTelegram канал: https://t.me/vidowsov100500\nПаблик +100500 ВКонтакте: https://vk.com/maximplus100500\nMoran Days (Второй Канал) : http://www.youtube.com/user/MoranDays\nTwitter: http://twitter.com/maxplus100500\n\nВидео из эпизода: https://vk.com/wall-1719791_1909121\n\n0:00 БАНАНОВАЯ ХИТРОСТЬ\n1:11 ИНТРО \n1:28 ИГРУШКИ ДЬЯВОЛА\n4:29 ВНЕЗАПНЫЙ ЛЕОПАРД\n6:13 ХЛЕБНЫЙ ГОЛУБЬ\n7:27 ЛЫСЫЕ ДЕНЬГИ\n9:04 МУЗЫКАЛЬНЫЙ КОНЕЦ', duration=568)
    VideoInfo(id=456262820, owner_id=-1719791, title='ЛЮБОВЬ И КЕТЧУП ❤️🥫 / +100500', direct_url='https://vkvideo.ru/video-1719791_456262820?pl=-1719791_48513772', date=datetime.datetime(2023, 7, 11, 19, 39, 50), description='Эпизод # 531 :D\nTWITCH: https://www.twitch.tv/moran_plays\nTelegram канал MORAN PLAYS: https://t.me/MORANPLAYS\n\nTelegram канал: https://t.me/vidowsov100500\nПаблик +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\nMoran Days (Второй Канал) : http://www.youtube.com/user/MoranDays\nTwitter: http://twitter.com/maxplus100500\n\nВидео из эпизода: https://vk.com/wall-1719791_1903217\n\n0:00 НУЛЕВОЙ ВИДОС\n0:21 ИНТРО\n0:48 МАМА ЗЕВАЕТ\n2:28 VIP МУЖИК\n4:44 САМОПЛЮЙ\n6:44 ЛЮБОВЬ И КЕТЧУП\n8:19 ПРОЩАЛОЧКА\n8:58 МУЗЫКАЛЬНЫЙ КОНЕЦ\n9:30 СЦЕНА ПОСЛЕ ТИТРОВ', duration=593)
    VideoInfo(id=456262637, owner_id=-1719791, title='УАЗИК ПРОТИВ БАШНИ 🚛🗼 / +100500', direct_url='https://vkvideo.ru/video-1719791_456262637?pl=-1719791_48513772', date=datetime.datetime(2023, 5, 16, 18, 11, 35), description='Эпизод # 530 :D\nTelegram канал: https://t.me/vidowsov100500\nПаблик +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\nMoran Days (Второй Канал) : http://www.youtube.com/user/MoranDays\nTwitter: http://twitter.com/maxplus100500\n\nВидео из эпизода: https://vk.com/wall-1719791_1899721\n\n0:00 ИНТРО\n0:27 ВИСЯЧИЙ ПЕВЕЦ\n2:49 ЛАМПОЧКА И СЕМЁРКА\n5:33 УБЕРИ УАЗИК\n7:37 ДОМАШНИЙ ПИВОВАР\n11:01 ПРОЩАЛОЧКА\n11:19 МУЗЫКАЛЬНЫЙ КОНЕЦ\n11:43 СЦЕНА ПОСЛЕ ТИТРОВ', duration=744)
    VideoInfo(id=456263436, owner_id=-1719791, title='ПОЛНЫЙ ОТРЫВ БАРАНКИ 🛞 / +100500', direct_url='https://vkvideo.ru/video-1719791_456263436?pl=-1719791_48513772', date=datetime.datetime(2024, 2, 6, 1, 58, 22), description='Эпизод # 529 :D\nTelegram канал: https://t.me/vidowsov100500\nПаблик +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\nMoran Days (Второй Канал) : http://www.youtube.com/user/MoranDays\nTwitter: http://twitter.com/maxplus100500\n\nВидео из эпизода: https://vk.com/wall-1719791_1897424\n\n0:00 ИНТРО\n0:27 ФРОНТАЛКА\n2:09 РУБАНУЛ МОБИЛУ\n4:25 ОТОРВАЛ БАРАНКУ\n7:04 ЗАСТЫЛ\n9:11 ПРОЩАЛОЧКА\n9:39 МУЗЫКАЛЬНЫЙ КОНЕЦ\n10:08 СЦЕНА ПОСЛЕ ТИТРОВ', duration=633)
    """

    print()

    videos: list[VideoInfo] = get_first_videos(
        "https://vkvideo.ru/@maximplus100500/all"
    )
    _print_videos(videos)
    """
    Video (20):
    VideoInfo(id=456264517, owner_id=-1719791, title='ДАНИЛ КОЛБАСЕНКО / +100500', direct_url='https://vkvideo.ru/video-1719791_456264517', date=datetime.datetime(2026, 3, 3, 21, 7, 41), description='Эпизод # 554 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/ad53a66d-54d3-43f9-80a2-41242cb7da8d?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18769\n\n00:00 ДАНИЛ КОЛБАСЕНКО\n02:55 ИНТРО\n03:13 ГОЛУБЯТНЯ В ДЕСЯТКЕ\n05:02 ПАРУСА ИЗ КАНАЛИЗАЦИИ\n07:03 АРОМАТНЫЕ ПАЛЬЧИКИ\n09:22 МУЗЫКАЛЬНЫЙ КОНЕЦ\n\nПо вопросам рекламы: maks100500@didenokteam.com', duration=599)
    VideoInfo(id=456264471, owner_id=-1719791, title='Винегретная', direct_url='https://vkvideo.ru/video-1719791_456264471', date=datetime.datetime(2026, 2, 27, 19, 5, 5), description='♦ Наш Telegram канал:\nhttps://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nhttps://t.me/vidowsov100500\n\n00:02 - Командир вселенной \n00:49 - Беспилотный дрифт\n01:08 - Внезапное приветствие \n01:17 - Актёрище\n01:45 - Конь взбрыкнул\n01:58 - Сонное царство\n02:21 - Не трожь десерт\n02:33 - Трюк тиски\n02:45 - Моя тачка\n03:04 - Чудо дрифт\n03:13 - Это молоко\n03:27 - Комфортная темница\n04:34 - Нежнятина\n04:51 - Красотища\n05:07 - Кошка Соня\n05:36 - Музыкальный конец', duration=350)
    VideoInfo(id=456264467, owner_id=-1719791, title='КОТОНАРЕЗКА ПРИСУТСТВУЕТ', direct_url='https://vkvideo.ru/video-1719791_456264467', date=datetime.datetime(2026, 2, 22, 14, 9, 52), description='♦ Наш Telegram канал:\nhttps://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nhttps://t.me/vidowsov100500\n\n00:02 - КОТЫ\n01:07 - КОЗА (жадная)\n01:23 - КОТ (сычуаньский муд)\n01:34 - КОТ (жваловый)\n01:50 - ТОРЖЕСТВЕННЫЙ ПТИЦ\n02:23 - КОТОСЕМЕЙКА (рыбачит)\n03:08 - СОЛНЕЧНЫЕ ВАННЫ (?бибизян)\n03:26 - КОТЫ (у кормушки)', duration=258)
    VideoInfo(id=456264466, owner_id=-1719791, title='Романтичная Нарезка', direct_url='https://vkvideo.ru/video-1719791_456264466', date=datetime.datetime(2026, 2, 17, 19, 2, 31), description='♦ Наш Telegram канал:\nhttps://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nhttps://t.me/vidowsov100500\n\n00:02 - Призрачный гонщик\n00:18 - Припечатало буднично \n00:26 - Только показывает\n01:01 - Смятие кабины\n01:28 - Романтичная рыбалка\n01:53 - Мясной букет\n02:02 - Собачья левитация\n02:26 - Змея на горке\n02:47 - Кошачьи нежности\n03:55 - Котик спускается', duration=257)
    VideoInfo(id=456264461, owner_id=-1719791, title='Нарезка Заморезка', direct_url='https://vkvideo.ru/video-1719791_456264461', date=datetime.datetime(2026, 2, 11, 18, 20, 49), description='♦ Наш Telegram канал:\nhttps://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nhttps://t.me/vidowsov100500\n\n00:02 - Прохладная погода\n00:10 - Двадцатка за трюк\n00:24 - Вайбовая варежка\n00:36 - Микроволновка с радио\n01:00 - Выпуклый дом\n01:23 - Такси 2 авария\n02:17 - Балдёжный вид\n02:35 - Обмен на рыбов\n02:46 - Комфортик такси\n03:03 - Сервер засыпало\n03:16 - Николаич позорит\n04:13 - Музыкальный конец', duration=274)
    ...
    VideoInfo(id=456264437, owner_id=-1719791, title='ОБЛЕЗЛЫЙ НОВЫЙ ГОД 🎄 Ёлка-Ёршик и Розетки На Ковре', direct_url='https://vkvideo.ru/video-1719791_456264437', date=datetime.datetime(2025, 12, 31, 20, 22, 31), description='Эпизод # 552 :D\nBOOSTY (этот выпуск с дополнительным обзором на ещё одно видео): https://boosty.to/max100500/posts/f81d5f16-a3ea-4aac-8fc2-aacff72fb645?share=post_link\nTWITCH: https://www.twitch.tv/moran_plays\nTELEGRAM: https://t.me/vidowsov100500\nСООБЩЕСТВО +100500 ВКонтакте: https://vk.com/maximplus100500\nTikTok: https://www.tiktok.com/@maxim_golopolosov\n\nВидео из эпизода: https://t.me/vidowsov100500/18571\n\n00:00 НОВОГОДНИЙ ЁРШИК\n02:04 ИНТРО\n02:23 ДЕД МОРОЗ ПОЛОЖИЛ\n03:48 ОЛИВЬЕШНЫЙ ГРИНЧ\n05:23 КРЕАТИВНЫЙ ЭЛЕКТРИК\n07:48 ПОЗДРАВЛЕНИЕ\n08:49 МУЗЫКАЛЬНЫЙ КОНЕЦ', duration=554)
    VideoInfo(id=456264436, owner_id=-1719791, title='ПОСЛЕДНЯЯ Нарезка Хлеборезка', direct_url='https://vkvideo.ru/video-1719791_456264436', date=datetime.datetime(2025, 12, 30, 23, 26), description='♦ Наш Telegram канал:\nhttps://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nhttps://t.me/vidowsov100500', duration=476)
    VideoInfo(id=456264434, owner_id=-1719791, title='НГ Нарезки Хлеборезки', direct_url='https://vkvideo.ru/video-1719791_456264434', date=datetime.datetime(2025, 12, 29, 18, 21, 54), description='♦ Наш Telegram канал:\nhttps://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nhttps://t.me/vidowsov100500', duration=240)
    VideoInfo(id=456264431, owner_id=-1719791, title='Нарезной Батон', direct_url='https://vkvideo.ru/video-1719791_456264431', date=datetime.datetime(2025, 12, 25, 15, 28, 32), description='♦ Наш Telegram канал:\nhttps://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nhttps://t.me/vidowsov100500', duration=251)
    VideoInfo(id=456264428, owner_id=-1719791, title='Нарезки Хлеборезки', direct_url='https://vkvideo.ru/video-1719791_456264428', date=datetime.datetime(2025, 12, 20, 18, 53, 54), description='♦ Наш Telegram канал:\nhttps://t.me/joinchat/AAAAAFN0AdiHBwyVZ2GWTw\nhttps://t.me/vidowsov100500', duration=235)
    """
