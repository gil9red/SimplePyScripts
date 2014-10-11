__author__ = 'ipetrash'


"""Получение списка запущенных процессов."""


if __name__ == '__main__':
    import psutil

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            print(pinfo)