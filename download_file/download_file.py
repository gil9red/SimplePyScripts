__author__ = "ipetrash"


"""Способы скачивания файлов с сайтов."""


import time
from urllib.request import urlopen, urlretrieve

# pip install httplib2
import httplib2

# pip install requests
import requests

# pip install grab
from grab import Grab


def timer(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        r = f(*args, **kwargs)
        print(f"Время выполнения функции: {time.time() - t:f} сек.")
        return r

    return wrapper


@timer
def way1(url: str, file_name: str) -> None:
    resource = urlopen(url)
    with open(file_name, "wb") as f:
        f.write(resource.read())


@timer
def way2(url: str, file_name: str) -> None:
    urlretrieve(url, file_name)


@timer
def way3(url: str, file_name: str) -> None:
    p = requests.get(url)
    with open(file_name, "wb") as f:
        f.write(p.content)


@timer
def way4(url: str, file_name: str) -> None:
    h = httplib2.Http(".cache")
    response, content = h.request(url)
    with open(file_name, "wb") as f:
        f.write(content)


@timer
def way5(url: str, file_name: str) -> None:
    g = Grab()
    g.go(url)
    g.response.save(file_name)


if __name__ == "__main__":
    url_img = "https://github.com/gil9red/telegram__random_bashim_bot/blob/b24139b536abf5b217b316405bbe224bc473fbfa/screenshots/screenshot_comics.jpg"

    way1(url_img, "img1.jpg")
    way2(url_img, "img2.jpg")
    way3(url_img, "img3.jpg")
    way4(url_img, "img4.jpg")
    way5(url_img, "img5.jpg")
