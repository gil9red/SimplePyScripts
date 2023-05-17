__author__ = "ipetrash"


"""
Пример того как можно узнать свой ip,
используя запрос на сайт и модуль grab.
"""


from grab import Grab


def get_my_public_ip() -> str:
    g = Grab()
    g.setup(proxy="proxy.compassplus.ru:3128", proxy_type="http")
    g.go("http://api.wipmania.com")
    context = g.doc.body.decode("utf-8")
    return context.split("<br>")[0]


if __name__ == "__main__":
    ip = get_my_public_ip()
    print(f"My IP: {ip}")
