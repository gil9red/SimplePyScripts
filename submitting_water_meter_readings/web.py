#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer, DEFAULT_ERROR_MESSAGE
import traceback
import os.path
from urllib.parse import urlsplit, parse_qs

# pip install selenium
from selenium import webdriver

import db


db.init_db()


def open_web_page_mail(value_cold: int, value_hot: int) -> (bool, str):
    # Example: 123 -> 00123
    value_cold = str(value_cold).zfill(5)
    value_hot = str(value_hot).zfill(5)

    profile_directory = r'%AppData%\Mozilla\Firefox\Profiles\p75l82q1.for_mail__selenium'
    profile = webdriver.FirefoxProfile(os.path.expandvars(profile_directory))

    driver = webdriver.Firefox(profile)
    driver.implicitly_wait(20)  # seconds
    driver.get('https://e.mail.ru/templates/')
    print(f'Title: {driver.title!r}')

    items = [item for item in driver.find_elements_by_css_selector('a[href*="/templates/"]') if 'vodomer' in item.text]
    if not items:
        text = 'Шаблон с "vodomer" не найден'
        print(text)
        return False, text

    items[0].click()

    print(f'Title: {driver.title!r}')

    editor = driver.find_element_by_css_selector('[role="textbox"]')
    template_text = editor.text

    if 'value_cold' not in template_text and 'value_hot' not in template_text:
        text = 'В шаблоне не найдены "value_cold" и "value_hot"'
        print(text)
        return False, text

    mail_text = template_text \
        .replace('value_cold', value_cold) \
        .replace('value_hot', value_hot)

    # Заполнение текста письма
    editor.clear()
    editor.send_keys(mail_text)

    return True, ''


TITLE = "Отправка показаний водомеров"
HEADERS = ["#", "Дата", "Холодная", "Горячая"]

HTML_CSS = """\
    <style type="text/css">
        table {
            border-collapse: collapse; /* Убираем двойные линии между ячейками */
            width: 100%;
        }
            .frame th {
                font-size: 110%;
            }
            .frame td, .frame th {
                border: 1px double #333; /* Рамка таблицы */
                padding: 5px;
            }

        form label {
            clear: both;
        }
        form input {
            width: 100%;
            margin-bottom: 10px;
        }
        form button {
            width: 100%;
        }
        
        .error_message {
            font-size: 120%;
            color: red;
            font-weight: bold;
            text-align: center;
            padding: 6px;
        }
    </style>
"""
HTML_TEMPLATE_INDEX = """\
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>{{ title }}</title>
    {{ HTML_CSS }}
</head>
<body>
    <div>
        <h3 align="center">{{ title }}</h3>

        <form method="post">
            <fieldset>
                <legend>Данные по воде:</legend>
                <div>
                    <label>Холодная:
                    <input type="number" min="0" max="99999" name="value_cold" id="value_cold" required>
                    </label>
                </div>
                <div>
                    <label>Горячая:
                    <input type="number" min="0" max="99999" name="value_hot" id="value_hot" required>
                    </label>
                </div>
                <div>
                    <button>Отправить</button>
                </div>
            </fieldset>
        </form>

        <br><hr><br>
        
        <table class="frame">
            <colgroup>
                <col span="1">
            </colgroup>
            <tbody>
                <tr>
                    {{ headers }}
                </tr>
                {{ table_rows }}
            </tbody>
        </table>
    </div>
</body>
</html>
""".replace('{{ HTML_CSS }}', HTML_CSS).replace('{{ title }}', TITLE)\
    .replace('{{ headers }}', ''.join(f'<th>{x}</th>' for x in HEADERS)) \

HTML_TEMPLATE_SEND_AGAIN = """\
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>{{ title }}</title>
    {{ HTML_CSS }}
</head>
<body>
    <div>
        <h3 align="center">{{ title }}</h3>
        <div class="error_message">{{ error_message }}</div>

        <form method="post">
            <fieldset>
                <legend>Данные по воде:</legend>
                <div>
                    <label>Холодная:
                    <input type="number" min="0" max="99999" name="value_cold" id="value_cold" value="{{ value_cold }}" required>
                    </label>
                </div>
                <div>
                    <label>Горячая:
                    <input type="number" min="0" max="99999" name="value_hot" id="value_hot" value="{{ value_hot }}" required>
                    </label>
                </div>
                <input id="forced" name="forced" type="hidden" value="">
                <div>
                    <button style="font-size: 130%; font-weight: bold">Все равно отправить?</button>
                    <div style="height: 10px"></div>
                    <button type="button" onclick="window.location.href='/'">Вернуться на главную страницу</button>
                </div>
            </fieldset>
        </form>
    </div>
</body>
</html>
""".replace('{{ HTML_CSS }}', HTML_CSS).replace('{{ title }}', TITLE)


class HttpProcessor(BaseHTTPRequestHandler):
    error_message_format = DEFAULT_ERROR_MESSAGE.replace(
        '<head>', '<head><meta name="viewport" content="width=device-width, initial-scale=1">'
    )

    def parse_POST(self):
        # SOURCE: https://stackoverflow.com/a/4233452/5909792
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            data = self.rfile.read(length).decode('utf-8')
            postvars = parse_qs(data, keep_blank_values=True)
        else:
            postvars = dict()

        return postvars

    def do_GET(self):
        o = urlsplit(self.path)

        # Only index
        if o.path != '/':
            self.send_error(404)
            return

        table_rows = []
        for i, x in reversed(list(enumerate(db.get_all(reversed=False), 1))):
            table_rows.append(f'''
            <tr>
                <td>{i}</td>
                <td>{x['date']}</td>
                <td>{str(x['cold']).zfill(5)}</td>
                <td>{str(x['hot']).zfill(5)}</td>
            </tr>
            ''')

        text = HTML_TEMPLATE_INDEX \
            .replace('{{ table_rows }}', ''.join(table_rows))

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Connection', 'close')
        self.end_headers()

        self.wfile.write(text.encode('utf-8'))

    def do_POST(self):
        o = urlsplit(self.path)

        # Only index
        if o.path != '/':
            self.send_error(404)
            return

        postvars = self.parse_POST()
        if 'value_cold' not in postvars or 'value_hot' not in postvars:
            self.send_error(400, explain='Не найдены параметры запроса value_cold и value_hot')
            return

        try:
            value_cold = postvars.get('value_cold')[0]
            value_hot = postvars.get('value_hot')[0]
            forced = 'forced' in postvars
            try:
                value_cold = int(value_cold)
                value_hot = int(value_hot)
            except ValueError:
                self.send_error(400, explain='Параметры запроса value_cold и value_hot должны быть числами')
                return

            # Проверка находится после open_web_page_mail, чтобы была возможность отправить письмо
            if not db.add(value_cold, value_hot, forced):
                message = 'Попытка повторной отправки показания за тот же месяц'
                text = HTML_TEMPLATE_SEND_AGAIN\
                    .replace('{{ error_message }}', message)\
                    .replace('{{ value_cold }}', str(value_cold))\
                    .replace('{{ value_hot }}', str(value_hot))

                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Connection', 'close')
                self.end_headers()

                self.wfile.write(text.encode('utf-8'))
                return

            ok, err_text = open_web_page_mail(value_cold, value_hot)
            if not ok:
                db.delete_last()
                self.send_error(500, explain=err_text)

            # Redirect to index
            self.send_response(302)
            self.send_header('Location', '/')
            self.send_header('Connection', 'close')
            self.end_headers()

        except:
            text = traceback.format_exc()
            self.send_error(500, explain=text)


def run(server_class=HTTPServer, handler_class=HttpProcessor, host='127.0.0.1', port=8080):
    print(f"HTTP server running on http://{'127.0.0.1' if host == '0.0.0.0' else host}:{port}")
    server_address = (host, port)

    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run(
        server_class=ThreadingHTTPServer,
        host='0.0.0.0', port=10014
    )
