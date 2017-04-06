# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#
# __author__ = 'ipetrash'
#
#
# # TODO: костыль для винды, для исправления проблем с исключениями
# # при выводе юникодных символов в консоль винды
# # Возможно, не только для винды, но и для любой платформы стоит использовать
# # эту настройку -- мало какие проблемы могут встретиться
# import sys
# if sys.platform == 'win32':
#     import codecs
#     sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach(), 'backslashreplace')
#     sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.detach(), 'backslashreplace')
#
#
# import os
# from config import BACKUP_DIR_LIST, DB_FILE_NAME, BACKUP_GIST
#
#
# class WebUserAlertException(Exception):
#     """
#     Исключение, которое будет показано пользователю на странице.
#
#     Работает только для v2.
#
#     """
#
#
# FINISHED = 'Finished'
# FINISHED_WATCHED = 'Finished watched'
#
#
# if BACKUP_GIST:
#     for path in BACKUP_DIR_LIST:
#         if not os.path.exists(path):
#             try:
#                 os.mkdir(path)
#
#             except FileNotFoundError as e:
#                 print(e)
#                 import traceback
#                 print(traceback.format_exc())
#
#
# def create_connect():
#     import sqlite3
#     return sqlite3.connect(DB_FILE_NAME)
#
#
# def db_create_backup():
#     for path in BACKUP_DIR_LIST:
#         from datetime import datetime
#         file_name = str(datetime.today().date()) + '.sqlite'
#         file_name = os.path.join(path, file_name)
#
#         import shutil
#         shutil.copy(DB_FILE_NAME, file_name)
#
#
# def get_games_by_kind(kind: str) -> [(int, str, str)]:
#     """
#     Функция возвращает список игр как кортеж из (id, name, price)
#
#     """
#
#     connect = create_connect()
#
#     try:
#         cursor = connect.cursor()
#
#         get_game_sql = '''
#             SELECT id, name, price
#             FROM game
#             WHERE kind = ?
#             ORDER BY name
#         '''
#         return cursor.execute(get_game_sql, (kind,)).fetchall()
#
#     finally:
#         connect.close()
#
#
# def get_finished_games() -> [(int, str, str)]:
#     """
#     Функция возвращает список завершенных игр как кортеж из (id, name, price)
#
#     """
#
#     return get_games_by_kind(FINISHED)
#
#
# def get_finished_watched_games() -> [(int, str, str)]:
#     """
#     Функция возвращает список просмотренных игр как кортеж из (id, name, price)
#
#     """
#
#     return get_games_by_kind(FINISHED_WATCHED)
#
#
# def get_id_games_by_name(game_name: str) -> list:
#     """
#     Функция возвращает список id игр.
#
#     """
#
#     connect = create_connect()
#     try:
#         cursor = connect.cursor()
#
#         # Получение id игр с указанным названием
#         return [id_ for (id_,) in cursor.execute("SELECT id FROM Game WHERE name = ?", (game_name,)).fetchall()]
#
#     finally:
#         connect.close()
#
#
# def set_price_game(game: str, price: str) -> list:
#     """
#     Функция найдет игры с указанным названием и изменит их цену в базе.
#     Возвращает список id игр с измененной ценой.
#
#     """
#
#     game = game.strip()
#     price = price.strip()
#
#     if not game or not price:
#         error_text = 'Не указано game ( = "{}") или price ( = "{}")'.format(game, price)
#         print(error_text)
#         raise WebUserAlertException(error_text)
#
#     connect = create_connect()
#     try:
#         cursor = connect.cursor()
#         cursor.execute("UPDATE Game SET price = ?, modify_date = date('now') WHERE name = ?", (price, game))
#         connect.commit()
#
#         # Получение id игр с указанным названием
#         return get_id_games_by_name(game)
#
#     finally:
#         connect.close()
#
#
# def rename_game(old_name: str, new_name: str) -> dict:
#     """
#     Функция меняет название указанной игры и возвращает словарь с результатом работы.
#
#     """
#
#     old_name = old_name.strip()
#     new_name = new_name.strip()
#
#     if not old_name or not new_name:
#         error_text = 'Не указано old_name ( = "{}") или new_name ( = "{}")'.format(old_name, new_name)
#         print(error_text)
#         raise WebUserAlertException(error_text)
#
#     connect = create_connect()
#     try:
#         cursor = connect.cursor()
#
#         has = cursor.execute("SELECT 1 FROM Game WHERE name = ?", (new_name,)).fetchone()
#         if has:
#             error_text = 'Нельзя переименовать "{}", т.к. имя "{}" уже занято'.format(old_name, new_name)
#             print(error_text)
#             raise WebUserAlertException(error_text)
#
#         cursor.execute("UPDATE Game SET name = ? WHERE name = ?", (new_name, old_name))
#         connect.commit()
#
#         # Получение id игр с указанным названием
#         id_games_with_changed_name = get_id_games_by_name(new_name)
#
#         # Попытаемся после переименования игры сразу найти ее цену
#         id_games_with_changed_price, price = check_and_fill_price_of_game(new_name)
#
#         result = {
#             'id_games_with_changed_name': id_games_with_changed_name,
#             'id_games_with_changed_price': id_games_with_changed_price,
#             'new_name': new_name,
#             'price': price,
#         }
#         return result
#
#     finally:
#         connect.close()
#
#
# def delete_game(name: str, kind: str) -> int:
#     """
#     Функция удаляет указанную игру и возвращает ее id.
#     Возможна отправка исключения <WebUserAlertException> при ошибке.
#
#     """
#
#     try:
#         if not name or not kind or (kind != FINISHED and kind != FINISHED_WATCHED):
#             error_text = 'Не указано name ( = "{}") или kind ( = "{}"), ' \
#                          'или kind неправильный (может быть {} или {}).'.format(name, kind, FINISHED, FINISHED_WATCHED)
#             print(error_text)
#             raise WebUserAlertException(error_text)
#
#         connect = create_connect()
#
#         id_game = connect.execute("SELECT id FROM Game WHERE kind = ? AND name = ?", (kind, name)).fetchone()
#         if not id_game:
#             error_text = 'Не получилось найти игру с name ( = "{}") и kind ( = "{}")'.format(name, kind)
#             print(error_text)
#             raise WebUserAlertException(error_text)
#
#         id_game = id_game[0]
#
#         connect.execute("DELETE FROM Game WHERE id = ?", (id_game,))
#         connect.commit()
#
#         return id_game
#
#     except WebUserAlertException as e:
#         raise e
#
#     except Exception as e:
#         error_text = 'При удалении игры "{}" ({}) произошла ошибка: {}'.format(name, kind, e)
#         raise WebUserAlertException(error_text)
#
#     finally:
#         connect.close()
#
#
# def set_check_game_by_steam(game: str, check=1):
#     game = game.strip()
#
#     connect = create_connect()
#     try:
#         cursor = connect.cursor()
#         cursor.execute("UPDATE Game SET check_steam = ? WHERE name = ?", (check, game))
#         connect.commit()
#
#     finally:
#         connect.close()
#
#
# def get_duplicates() -> list:
#     from collections import defaultdict
#     name_kind_by_id_dict = defaultdict(list)
#
#     connect = create_connect()
#     try:
#         for id_, name, kind in connect.cursor().execute('SELECT id, name, kind FROM game').fetchall():
#             name_kind_by_id_dict[(name, kind)].append(id_)
#
#     finally:
#         connect.close()
#
#     return list(filter(lambda item: len(item[1]) > 1, name_kind_by_id_dict.items()))
#
#
# def check_price_all_non_price_games() -> list:
#     """
#     Принудительная проверка цены у игр без цены. То, что цены игр уже проверялись для этой функции
#     значение не имеет.
#
#     """
#
#     connect = create_connect()
#     try:
#         # Список игр с измененной ценой
#         games_with_changed_price = list()
#
#         games = connect.cursor().execute('SELECT name FROM game WHERE price IS NULL').fetchall()
#
#         # Удаление дубликатов (игры могут повторяться для категорий пройденных и просмотренных)
#         games = {name for (name,) in games}
#         print('Игр без цены: {}'.format(len(games)))
#
#         for name in games:
#             id_games, price = check_and_fill_price_of_game(name)
#             if price is not None:
#                 games_with_changed_price.append((id_games, name, price))
#
#             import time
#             time.sleep(3)
#
#         return games_with_changed_price
#
#     finally:
#         connect.close()
#
#
# def get_games_list() -> list:
#     """
#     Функция возвращает кортеж из двух списков: список пройденных игр и список просмотренных игр
#
#     """
#
#     # Пройденные игры
#     finished_game_list = list()
#
#     # Просмотренные игры
#     finished_watched_game_list = list()
#
#     import requests
#     rs = requests.get('https://gist.github.com/gil9red/2f80a34fb601cd685353')
#
#     from bs4 import BeautifulSoup
#     root = BeautifulSoup(rs.content, 'lxml')
#     href = root.select_one('.file-actions > a')['href']
#
#     from urllib.parse import urljoin
#     raw_url = urljoin(rs.url, href)
#
#     rs = requests.get(raw_url)
#     content_gist = rs.text
#
#     # Скрипт может сохранять скачанные гисты
#     if BACKUP_GIST:
#         for path in BACKUP_DIR_LIST:
#             from datetime import datetime
#             file_name = str(datetime.today().date()) + '.txt'
#             file_name = os.path.join(path, file_name)
#
#             with open(file_name, 'w', encoding='utf-8') as f:
#                 f.write(content_gist)
#
#     # Для поиска игр, относящихся только к PC
#     found_pc = False
#
#     # Перебор строк файла
#     for line in content_gist.splitlines():
#         # Удаление пустых символов справа (пробелы, переводы на следующую строку и т.п.)
#         line = line.rstrip()
#
#         # Если строка пустая
#         if not line:
#             continue
#
#         # Проверка, что первым символом не может быть флаг для игр и что последним символом будет :
#         # Т.е. ищем признак платформы
#         if line[0] not in [' ', '-', '@'] and line.endswith(':'):
#             # Если встретили PC
#             found_pc = line == 'PC:'
#             continue
#
#         name = line[2:].rstrip()
#         games = parse_game_name(name)
#
#         # Теперь, осталось добавить игру
#         if found_pc:
#             # Пройденные игры
#             if line.startswith('  '):
#                 finished_game_list += games
#
#             # Просмотренные игры
#             elif line.startswith('@ ') or line.startswith(' @'):
#                 finished_watched_game_list += games
#
#     return finished_game_list, finished_watched_game_list
#
#
# def append_games_to_base(connect, finished_game_list, finished_watched_game_list):
#     """
#     Функция для добавление игр в таблицу базы. Если игра уже есть в базе, то запрос игнорируется.
#
#     """
#
#     cursor = connect.cursor()
#
#     def insert_game(name, kind):
#         # Для отсеивания дубликатов
#         has = cursor.execute("SELECT 1 FROM Game WHERE name = ? and kind = ?", (name, kind)).fetchone()
#         if has:
#             return
#
#         print('Добавляю новую игру "{}" ({})'.format(name, kind))
#         cursor.execute("INSERT INTO Game (name, kind) VALUES (?,?)", (name, kind))
#
#     # Добавлени в базу пройденных игр
#     for name in finished_game_list:
#         insert_game(name, FINISHED)
#
#     # Добавлени в базу просмотренных игр
#     for name in finished_watched_game_list:
#         insert_game(name, FINISHED_WATCHED)
#
#     # Сохранение изменений в базе
#     connect.commit()
#
#     # Вряд ли такое произойдет...
#     duplicates = get_duplicates()
#     if duplicates:
#         print("АХТУНГ! Найдены дубликаты:")
#         for (name, kind), id_list in duplicates:
#             print('    {} / {} c id {}'.format(name, kind, id_list))
#
#         print()
#
#
# def check_and_fill_price_of_game(game: str) -> (list, str):
#     """
#     Функция ищет цену игры и при нахождении ее ставит ей цену в базе.
#     Возвращает кортеж из списка id игр с измененной ценой и саму цену.
#
#     """
#
#     game = game.strip()
#
#     if not game:
#         print('Не указано game ( = "{}")'.format(game))
#         return list(), None
#
#     game_price = None
#
#     # Поищем игру и ее цену
#     game_price_list = steam_search_game_price_list(game)
#
#     # Отметим что игра искалась в стиме
#     set_check_game_by_steam(game)
#
#     # Сначала пытаемся найти игру по полному совпадению
#     for name, price in game_price_list:
#         if game == name:
#             game_price = price
#             break
#
#     # Если по полному совпадению на нашли, пытаемся найти предварительно очищая названия игр
#     # от лишних символов
#     if game_price is None:
#         for name, price in game_price_list:
#             # Если нашли игру, запоминаем цену и прерываем сравнение с другими найденными играми
#             if smart_comparing_names(game, name):
#                 game_price = price
#                 break
#
#     if game_price == 0 or game_price is None:
#         # TODO: заполнять вручную или искать на других сайтах цену
#         print('Не получилось найти цену игры {}, price is {}'.format(game, game_price))
#         return list(), None
#
#     print('Нашли игру: {} ({}) -> {}'.format(game, name, game_price))
#     return set_price_game(game, game_price), game_price
#
#
# def fill_price_of_games(connect):
#     """
#     Функция проходит по играм в базе без указанной цены, пытается найти цены и если удачно, обновляет значение.
#
#     # TODO: больше сайтов поддержать, т.к. на стиме не все игры можно найти.
#     Сайтом для поиска цен является стим.
#
#     """
#
#     # Перебор игр и указание их цены
#     # Перед перебором собираем все игры и удаляем дубликаты (игры могут и просмотренными, и пройденными)
#     # заодно список кортежей из одного имени делаем просто списом имен
#
#     sql_text = 'SELECT name FROM game where price is null and check_steam = 0'
#
#     cursor = connect.cursor()
#     games_list = set(game for (game,) in cursor.execute(sql_text).fetchall())
#     print("Нужно найти цену {} играм".format(len(games_list)))
#
#     for game in games_list:
#         check_and_fill_price_of_game(game)
#
#         import time
#         time.sleep(3)
#
#
# # Регулярка вытаскивает выражения вида: 1, 2, 3 или 1-3, или римские цифры: III, IV
# import re
# PARSE_GAME_NAME_PATTERN = re.compile(r'(\d+(, ?\d+)+)|(\d+ *?- *?\d+)|([MDCLXVI]+(, ?[MDCLXVI]+)+)',
#                                      flags=re.IGNORECASE)
#
#
# def parse_game_name(game_name):
#     """
#     Функция принимает название игры и пытается разобрать его, после возвращает список названий.
#     Т.к. в названии игры может находиться указание ее частей, то функция разберет их.
#
#     Пример:
#         "Resident Evil 4, 5, 6" станет:
#             ["Resident Evil 4", "Resident Evil 5", "Resident Evil 6"]
#
#         "Resident Evil 1-3" станет:
#             ["Resident Evil", "Resident Evil 2", "Resident Evil 3"]
#
#     """
#
#     match = PARSE_GAME_NAME_PATTERN.search(game_name)
#     if match is None:
#         return [game_name]
#
#     seq_str = match.group(0)
#     short_name = game_name.replace(seq_str, '').strip()
#
#     if ',' in seq_str:
#         seq = seq_str.replace(' ', '').split(',')
#
#     elif '-' in seq_str:
#         seq = seq_str.replace(' ', '').split('-')
#         if len(seq) > 2:
#             print('Unknown seq str = "{}".'.format(seq_str))
#         else:
#             seq = tuple(map(int, seq))
#             seq = tuple(range(seq[0], seq[1] + 1))
#     else:
#         print('Unknown seq str = "{}".'.format(seq_str))
#         return [game_name]
#
#     # Сразу проверяем номер игры в серии и если она первая, то не добавляем в названии ее номер
#     return [short_name if str(num) == '1' else '{} {}'.format(short_name, num) for num in seq]
#
#
# def steam_search_game_price_list(name):
#     """
#     Функция принимает название игры, после ищет его в стиме и возвращает результат как список
#     кортежей из (название игры, цена).
#
#     """
#
#     # category1 = 998 (Game)
#     # url = 'http://store.steampowered.com/search/?category1=998&os=win&supportedlang=english&term=' + name
#     #
#     # Дополнения с категорией Game не ищутся, например: "Pillars of Eternity: The White March Part I"
#     url = 'http://store.steampowered.com/search/?term=' + name
#
#     # TODO: проверить http://store.steampowered.com/search/suggest?term=Dig+or+Die&f=games&cc=RU&l=russian&no_violence=0&no_sex=0&v=2651658
#     # По идеи, это вариант запроса рабочий, но нужно потестить на разные ситуации: игры, DLC, как выглядят игры со скидкой и без
#
#     game_price_list = list()
#
#     # Из цикла не выйти, пока не получится скачать и распарсить страницу
#     while True:
#         try:
#             import requests
#             rs = requests.get(url)
#
#             from bs4 import BeautifulSoup
#             root = BeautifulSoup(rs.content, 'lxml')
#
#             break
#
#         except:
#             print('При поиске в стиме что-то пошло не так:')
#
#             import traceback
#             print(traceback.format_exc())
#
#             # Если произошла какая-то ошибка попытаемся через 5 минут попробовать снова
#             import time
#             time.sleep(5 * 60)
#
#     for div in root.select('.search_result_row'):
#         name = div.select_one('.title').text.strip()
#
#         # Ищем тег скидки
#         if div.select_one('.search_discount > span'):
#             price = div.select_one('.search_price > span > strike').text.strip()
#         else:
#             price = div.select_one('.search_price').text.strip()
#
#         # Если цены нет (например, игра еще не продается)
#         if not price:
#             price = None
#         else:
#             # Если в цене нет цифры считаем что это "Free To Play" или что-то подобное
#             import re
#             match = re.search(r'\d', price)
#             if not match:
#                 price = '0'
#             else:
#                 # Только значение цены
#                 if 'pуб' not in price:
#                     print('АХТУНГ! Неизвестный формат цены: "{}".'.format(price))
#
#                 price = price.replace(' pуб.', '').strip()
#
#         game_price_list.append((name, price))
#
#     return game_price_list
#
#
# def smart_comparing_names(name_1, name_2):
#     """
#     Функция для сравнивания двух названий игр.
#     Возвращает True, если совпадают, иначе -- False.
#
#     """
#
#     # Приведение строк к одному регистру
#     name_1 = name_1.lower()
#     name_2 = name_2.lower()
#
#     def clear_name(name):
#         import re
#         return re.sub(r'[^\w]', '', name).replace('_', '')
#
#     # Удаление символов кроме буквенных и цифр: "the witcher®3:___ вася! wild hunt" -> "thewitcher3васяwildhunt"
#     name_1 = clear_name(name_1)
#     name_2 = clear_name(name_2)
#
#     return name_1 == name_2
#
#
# class Settings:
#     """
#     Класс представляет собой таблицу в базе.
#
#     """
#
#     def __init__(self, connect):
#         # Сохраняем для работы с нашей таблицей в базе
#         self._connect = connect
#         self._cursor = self._connect.cursor()
#
#         # Создание таблицы для хранения настроек по типу: ключ - значение
#         self._cursor.execute('''
#         CREATE TABLE IF NOT EXISTS Settings (
#             key TEXT PRIMARY KEY,
#             value TEXT
#         );
#         ''')
#
#         self._connect.commit()
#
#     def __setattr__(self, key, value):
#         # TODO: так то нужно по другому проверять, что атрибут не является атрибутом самого класса
#         # Для обработки внутренних полей
#         if key.startswith("_"):
#             return super().__setattr__(key, value)
#
#         self._cursor.execute('INSERT OR REPLACE INTO Settings VALUES (?, ?);', (key, value))
#         self._connect.commit()
#
#     def __getattr__(self, key):
#         # TODO: так то нужно по другому проверять, что атрибут не является атрибутом самого класса
#         # Для обработки внутренних полей
#         if key.startswith("_"):
#             return super().__getattr__(key)
#
#         data = self._cursor.execute('SELECT value FROM Settings WHERE key = ?', (key,)).fetchone()
#         if data:
#             (value,) = data
#             return value
#
#     def keys(self):
#         return [key for (key,) in self._cursor.execute('SELECT key FROM Settings').fetchall()]
#
#     def values(self):
#         return [value for (value,) in self._cursor.execute('SELECT value FROM Settings').fetchall()]
#
#     def items(self):
#         return self._cursor.execute('SELECT key, value FROM Settings').fetchall()
