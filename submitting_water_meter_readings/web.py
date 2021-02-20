#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import cgi
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer, DEFAULT_ERROR_MESSAGE
from urllib.parse import urlsplit, urlparse, parse_qs
from os.path import splitext
from pathlib import Path

import db
from utils import open_web_page_water_meter, log


db.init_db()


DIR = Path(__file__).parent
PATH_STATIC = DIR / 'static'

MIME_BY_CONTENTYPE = {
    '.png': 'image/png',
    '.ico': 'image/x-icon',
    '.webmanifest': 'application/manifest+json',
}

ALLOW_LIST = [
    '/static/favicon/android-chrome-192x192.png',
    '/static/favicon/android-chrome-512x512.png',
    '/static/favicon/apple-touch-icon.png',
    '/static/favicon/favicon.ico',
    '/static/favicon/favicon-16x16.png',
    '/static/favicon/favicon-32x32.png',
    '/static/favicon/site.webmanifest',
]

TITLE = "Отправка показаний водомеров"
HEADERS = ["#", "Дата", "Холодная", "Горячая"]

HTML_CSS = (PATH_STATIC / 'style.css').read_text('utf-8')

HTML_TEMPLATE_INDEX = (PATH_STATIC / 'index.html').read_text('utf-8')\
    .replace('{{ HTML_CSS }}', HTML_CSS)\
    .replace('{{ title }}', TITLE)\
    .replace('{{ headers }}', ''.join(f'<th>{x}</th>' for x in HEADERS)) \

HTML_TEMPLATE_SEND_AGAIN = (PATH_STATIC / 'send_again.html').read_text('utf-8')\
    .replace('{{ HTML_CSS }}', HTML_CSS)\
    .replace('{{ title }}', TITLE)


def get_ext(url: str) -> str:
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext  # or ext[1:] if you don't want the leading '.'


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

        # Only index and ALLOW_LIST
        if o.path != '/' and o.path not in ALLOW_LIST:
            self.send_error(404)
            return

        if o.path in ALLOW_LIST:
            print('[o.path]', o.path)
            ext = get_ext(o.path)

            f = DIR / o.path.lstrip('/')
            data = f.read_bytes()

            self.send_response(200)
            self.send_header('Content-Type', MIME_BY_CONTENTYPE[ext])
            self.send_header('Content-length', len(data))
            self.end_headers()

            self.wfile.write(data)
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

            # Проверка находится после open_web_page_water_meter, чтобы была возможность отправить письмо
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

            ok, err_text = open_web_page_water_meter(value_cold, value_hot)
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
    log.info(f"HTTP server running on http://{'127.0.0.1' if host == '0.0.0.0' else host}:{port}")
    server_address = (host, port)

    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run(
        server_class=ThreadingHTTPServer,
        host='0.0.0.0', port=10014
    )
