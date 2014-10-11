__author__ = 'ipetrash'


if __name__ == '__main__':
    # Data Compression (модуль zlib_example)
    import zlib
    s = b'witch which has which witches wrist watch'
    print(s)
    print(len(s))
    t = zlib.compress(s)
    print(len(t))
    print(zlib.decompress(t))
    print(zlib.crc32(s))