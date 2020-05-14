#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# pip install psutil
import psutil

NEED_PROCESS = ['python.exe', 'pythonw.exe']
TITLE = "Список запущенных серверов на python"
HEADERS = ["#", "PID", "Порт(ы)", "Путь"]


class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        processes = []
        for proc in psutil.process_iter():
            if not proc.is_running() or proc.name().lower() not in NEED_PROCESS:
                continue

            connections = [c for c in proc.connections() if c.status == psutil.CONN_LISTEN and c.laddr]
            if not connections:
                continue

            connections.sort(key=lambda c: c.laddr.port)

            processes.append({
                'pid': proc.pid,
                'name': proc.name(),
                'path': os.path.normpath(proc.cmdline()[1]),
                'ports': ', '.join(str(c.laddr.port) for c in connections),
            })

        processes.sort(key=lambda p: int(''.join(c for c in p['ports'] if c.isdigit())))

        table_rows = []
        for i, p in enumerate(processes, 1):
            table_rows.append(f'''
            <tr {'class="grayscale"' if p['pid'] == os.getpid() else ''}>
                <td>{i}</td>
                <td>{p['pid']}</td>
                <td>{p['ports']}</td>
                <td>{p['path']}</td>
            </tr>
            ''')

        text = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
            <title>{{ title }}</title>

            <style type="text/css">
                table {
                    border-collapse: collapse; /* Убираем двойные линии между ячейками */
                }
                    /* Увеличим заголовок таблиц */
                    table > caption {
                        font-size: 150%;
                    }

                    .frame th {
                        font-size: 120%;
                    }
                    .frame td, .frame th {
                        border: 1px double #333; /* Рамка таблицы */
                        padding: 5px;
                    }

                .grayscale { 
                    color: grey;
                }
            </style>
        </head>
        <body>   
            <table class="frame" style="width: 1000px; margin:0 auto;">
                <caption>{{ title }}</caption>
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
        </body>
        </html>
        """ \
            .replace('{{ title }}', TITLE) \
            .replace('{{ headers }}', ''.join(f'<th>{x}</th>' for x in HEADERS)) \
            .replace('{{ table_rows }}', ''.join(table_rows))

        self.wfile.write(text.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=HttpProcessor, port=8080):
    print(f'HTTP server running on http://127.0.0.1:{port}')

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run(port=10012)
