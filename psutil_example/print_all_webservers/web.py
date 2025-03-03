#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from dataclasses import dataclass

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

# pip install psutil==6.1.0
import psutil


@dataclass
class Process:
    pid: int
    name: str
    path: str
    cwd: str
    ports: str


TITLE = "Список запущенных серверов"


def _get_processes() -> list[Process]:
    processes = []
    for proc in psutil.process_iter():
        try:
            connections = [
                c
                for c in proc.connections()
                if c.status == psutil.CONN_LISTEN and c.laddr
            ]
            if not connections:
                continue

            ports = sorted(set(c.laddr.port for c in connections))
            processes.append(
                Process(
                    pid=proc.pid,
                    name=proc.name(),
                    path=" ".join(os.path.normpath(x) for x in proc.cmdline()),
                    cwd=proc.cwd(),
                    ports=", ".join(map(str, ports)),
                )
            )

        except psutil.AccessDenied:
            pass

    processes.sort(key=lambda p: p.name)

    return processes


def get_html_info() -> str:
    table_rows: list[str] = [
        f"""
        <tr {'class="grayscale"' if p.pid == os.getpid() else ''}>
            <td>{i}</td>
            <td>{p.pid}</td>
            <td>{p.name}</td>
            <td class="ports"><div>{p.ports}</div></td>
            <td class="path"><div>{p.path}</div></td>
            <td class="cwd"><div>{p.cwd}</div></td>
        </tr>
        """
        for i, p in enumerate(_get_processes(), 1)
    ]

    text = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
        <title>{{ title }}</title>

        <style type="text/css">
            table {
                border-collapse: collapse; /* Убираем двойные линии между ячейками */
                width: 1200px;
                margin:0 auto;
            }
                /* Увеличим заголовок таблиц */
                table > caption {
                    font-size: 150%;
                }

                th {
                    font-size: 120%;
                    background: lightGrey;
                }
                td, th {
                    border: 1px double #333; /* Рамка таблицы */
                    padding: 5px;
                }
                td {
                    text-align: left;
                    vertical-align: top;
                }

                td.ports > div {
                    inline-size: 150px;
                }
                td.path > div {
                    inline-size: 400px;
                    overflow-wrap: break-word;
                }
                td.cwd > div {
                    inline-size: 300px;
                    overflow-wrap: break-word;
                }

            .grayscale { 
                color: grey;
            }
        </style>
    </head>
    <body>   
        <table>
            <caption>{{ title }}</caption>
            <thead>
                <tr>
                    <th>#</th>
                    <th>PID</th>
                    <th>Название</th>
                    <th>Порт(ы)</th>
                    <th>Путь</th>
                    <th>Cwd</th>
                </tr>
            </thead>
            <tbody>
                {{ table_rows }}
            </tbody>
        </table>
    </body>
    </html>
    """.replace(
        "{{ title }}", TITLE
    ).replace(
        "{{ table_rows }}", "\n".join(table_rows)
    )

    return text


class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        o = urlsplit(self.path)

        # Only index
        if o.path != "/":
            self.send_error(404)
            return

        text = get_html_info()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Connection", "close")
        self.end_headers()

        self.wfile.write(text.encode("utf-8"))


def run(server_class=HTTPServer, handler_class=HttpProcessor, port=8080):
    print(f"HTTP server running on http://127.0.0.1:{port}")

    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run(
        port=int(os.environ.get("PORT", 50012)),
    )
