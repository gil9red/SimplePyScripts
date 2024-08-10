#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from youtube_com__results_search_query import Playlist


URL = "https://www.youtube.com/playlist?list=PLC6A0625DCA9AAE2D"
NEED_SECONDS = 15 * 60  # 15 minutes

video_list = [
    video
    for video in Playlist.get_from(URL).video_list
    if video.duration_seconds >= NEED_SECONDS
]
for i, video in enumerate(video_list, 1):
    print(f"{i}. {video.title!r} ({video.duration_text}): {video.url}")

"""
1. '+100500 - ХЭЛЛОУИН В РОССИИ' (00:15:45): https://www.youtube.com/watch?v=rZd676uarvM&list=PLC6A0625DCA9AAE2D&index=1
2. '+100500 - ФУТБОЛИСТЫ КУРИЛЬЩИКА, НЕПРИСТОЙНЫЕ СООБЩЕНИЯ И КИБЕРДОМОФОН' (00:18:22): https://www.youtube.com/watch?v=_PpYcoLOLFc&list=PLC6A0625DCA9AAE2D&index=3
3. '+100500 - ГРИБНАЯ БРОНЬ, СОН В ГРОБУ, АДСКИЙ ТУАЛЕТ И КАЗАЧЬЯ ПОРКА' (00:18:39): https://www.youtube.com/watch?v=piyHbOtLQ6c&list=PLC6A0625DCA9AAE2D&index=4
4. '+100500 - ТУЛЬСКИЙ ПРЯНИК МЧСНИК' (00:22:54): https://www.youtube.com/watch?v=p-ctYnHkl7Y&list=PLC6A0625DCA9AAE2D&index=5
5. '10 ЛЕТ +100500 - 10 КЛАССИЧЕСКИХ ВИДОСОВ' (00:32:54): https://www.youtube.com/watch?v=L4OvXrraPkM&list=PLC6A0625DCA9AAE2D&index=34
6. '+100500 - НОВЫЕ ПОЛНОМОЧИЯ ПОЛИЦЕЙСКИХ И ЯБЛОКИ В КУРИНОМ БУЛЬОНЕ' (00:15:24): https://www.youtube.com/watch?v=u-qxgWLyWOw&list=PLC6A0625DCA9AAE2D&index=48
7. 'Реакция с Юджином - БЕЗУМНЫЙ СОСЕД И ЛОШАДИНОЕ РЖАНИЕ' (00:16:41): https://www.youtube.com/watch?v=Gp1El-Iwzms&list=PLC6A0625DCA9AAE2D&index=70
8. '+100500 - Валерий Полстакана' (00:15:14): https://www.youtube.com/watch?v=aL4WHs3ismg&list=PLC6A0625DCA9AAE2D&index=71
9. '+100500 - Обряд Привораживания (любовный приворот)' (00:15:43): https://www.youtube.com/watch?v=tllpuCzq0V8&list=PLC6A0625DCA9AAE2D&index=99
10. '+100500 - А КАК НАСЧЁТ ПОПЫ?' (00:15:43): https://www.youtube.com/watch?v=FQ1eRwAvIRY&list=PLC6A0625DCA9AAE2D&index=110
11. '+100500 - Алкаша Чуть Не Сбила Электричка + Интервью с "Чувак, Это Рэпчик!"' (00:17:49): https://www.youtube.com/watch?v=f4LklR-ohpQ&list=PLC6A0625DCA9AAE2D&index=146
12. '+100500 - Передёргивание На Первом' (00:16:43): https://www.youtube.com/watch?v=PfeWX-6Y6Xo&list=PLC6A0625DCA9AAE2D&index=148
13. '+100500 - Изгнание Демонов в Прямом Эфире' (00:17:25): https://www.youtube.com/watch?v=S-q-2hwSFis&list=PLC6A0625DCA9AAE2D&index=151
"""
