__author__ = "ipetrash"


"""Способы скачивания файлов с сайтов."""


def timer(f):
    def wrapper(*args, **kwargs):
        import time

        t = time.time()
        r = f(*args, **kwargs)
        print("Время выполнения функции: %f сек." % (time.time() - t))
        return r

    return wrapper


@timer
def way1(url, file_name):
    from urllib.request import urlopen

    resource = urlopen(url)
    with open(file_name, "wb") as f:
        f.write(resource.read())


@timer
def way2(url, file_name):
    from urllib.request import urlretrieve

    urlretrieve(url, file_name)


@timer
def way3(url, file_name):
    import requests

    p = requests.get(url)
    with open(file_name, "wb") as f:
        f.write(p.content)


@timer
def way4(url, file_name):
    import httplib2

    h = httplib2.Http(".cache")
    response, content = h.request(url)
    with open(file_name, "wb") as f:
        f.write(content)


@timer
def way5(url, file_name):
    from grab import Grab

    g = Grab()
    g.go(url)
    g.response.save(file_name)


if __name__ == "__main__":
    url_img = "http://shikimori.org/images/character/original/55741.jpg"

    way1(url_img, "img1.jpg")
    way2(url_img, "img2.jpg")
    way3(url_img, "img3.jpg")
    way4(url_img, "img4.jpg")
    way5(url_img, "img5.jpg")
