__author__ = 'ipetrash'


"""Получение списка запущенных процессов."""


# TODO: больше примеров по модулю psutil_example.
# Ссылки:
#   http://pythonhosted.org/psutil_example/
#   https://github.com/giampaolo/psutil_example


if __name__ == '__main__':
    import psutil

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            print(pinfo)
