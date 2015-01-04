import argparse
from datetime import datetime
import vk_api
import sys
import requests
from grab import Grab
import time
import urllib.parse

__author__ = 'ipetrash'


# Скрипт получает цитату с сайта bash.im и помещает ее на стену пользователя vk.com
# The script receives a quote from the site bash.im and puts it on the wall by vk.com


def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&quot;", '"')
    s = s.replace("&apos;", "'")
    s = s.replace("&amp;", "&")
    return s


def bash_quote():
    rs = requests.get('http://bash.im/random')
    g = Grab(rs.text)

    quote = g.doc.select('//div[@class="quote"]')

    html_quote = quote.select('div[@class="text"]').html()

    quote_text = html_quote.replace('<div class="text">', '').replace('</div>', '')
    quote_text = unescape(quote_text)
    quote_text = quote_text.replace('<br>', '\n').strip()

    quote_href = quote.select('div/a[@class="id"]').attr('href')
    quote_href = urllib.parse.urljoin('http://bash.im/', quote_href)

    return quote_text, quote_href


def create_parser():
    parser = argparse.ArgumentParser(description="The script receives a quote from the site bash.im "
                                                 "and puts it on the wall by vk.com")
    parser.add_argument("login", help="Login from which the message will be sent.")
    parser.add_argument("psw", help="User password.")
    parser.add_argument("owner_id", help="ID on who will get the message.")
    parser.add_argument("-timeout", type=int, default=3600, help="The frequency of sending messages in seconds."
                                                                 "\nDefault 3600 sec.")
    return parser


def vk_auth(login, password):
    try:
        vk = vk_api.VkApi(login, password)  # Авторизируемся
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)  # В случае ошибки выведем сообщение
        sys.exit()

    return vk


if __name__ == '__main__':
    parser = create_parser()

    # Если не указаны параметры, выводим справку и выходим
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    # Авторизируемся
    vk = vk_auth(args.login, args.psw)

    while True:
        # Получаем текст цитаты и ее адрес
        quote_text, quote_href = bash_quote()

        # Добавление сообщения на стену пользователя id равным OWNER_ID
        # Если не указывать owner_id, сообщения себе на стену поместится
        rs = vk.method('wall.post', {
            'owner_id': args.owner_id,
            'message': quote_href + '\n\n' + quote_text,
        })

        cur_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('{}: post_id: {}, quote: {}'.format(cur_date, rs['post_id'], quote_href))

        time.sleep(args.timeout)  # Задержка в timeout секундах