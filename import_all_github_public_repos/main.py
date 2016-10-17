#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from config import *

# TODO: сделать версию с gui
# TODO: показывать процесс скачивания
# TODO: проверить для репозиториев с разными ветками
# TODO: проверить существование юзера
# TODO: многопоточность?
# TODO: настройка нужны ли форки и приватные импортировать
#       если логин/пароль не указан приватные не могут быть доступны и нужно ругаться
# TODO: если не указывать юзера при запросе репозиториев, но гитхаб выдаст репозитории, в которых
#       участвовал юзер, например в группе, возможно, их тоже нужно импортировать

# TODO: Ошибка:
# Repository(full_name="gil9red/QRcodeGen") https://api.github.com/repos/gil9red/QRcodeGen
# Traceback (most recent call last):
#   File "C:/Users/ipetrash/Documents/GitHub/SimplePyScripts/import_all_github_public_repos/main.py", line 66, in <module>
#     os.makedirs(REPOS_DIR)
#   File "C:/Users/ipetrash/Documents/GitHub/SimplePyScripts/import_all_github_public_repos/main.py", line 45, in get_repo
#
#   File "C:\Users\ipetrash\AppData\Local\Continuum\Anaconda3\lib\site-packages\git\remote.py", line 762, in pull
#     res = self._get_fetch_info_from_stderr(proc, progress)
#   File "C:\Users\ipetrash\AppData\Local\Continuum\Anaconda3\lib\site-packages\git\remote.py", line 640, in _get_fetch_info_from_stderr
#     finalize_process(proc, stderr=stderr_text)
#   File "C:\Users\ipetrash\AppData\Local\Continuum\Anaconda3\lib\site-packages\git\util.py", line 155, in finalize_process
#     proc.wait(**kwargs)
#   File "C:\Users\ipetrash\AppData\Local\Continuum\Anaconda3\lib\site-packages\git\cmd.py", line 335, in wait
#     raise GitCommandError(self.args, status, errstr)
# git.exc.GitCommandError: 'git pull -v origin' returned with exit code 1
# stderr: 'fatal: unable to access 'https://github.com/gil9red/QRcodeGen/': Received HTTP code 503 from proxy after CONNECT'

# TODO: поддержка архивации всей папки: к названию папки просто добавить zip
# TODO: поддержка импорта в дропбокс (хотя бы сохранение репозиториев в папку синхронизации дропбокса)
# TODO: поддержка импорта в гугл-диск (можно просто архив кидать)
#       импорт делать только при наличии изменений -- новые репозитории или изменение текущих
#       удаление репозиториев на гитхабе не удаляет репозитории на диске
# TODO: поддержка импорта в яндекс-диск
# TODO: поддержка импорта в облако-мейл: https://cloud.mail.ru/home/

# TODO: поддержка запароливания и шифрования репозиториев (особенно это касается приватных)
# TODO: поддержка уведомления на почту при импортировании


# TODO: дать более подходящее название
def get_repo(url, repos_dir, branch='master'):
    # Если закончивается url на .git
    len_url = len(url)
    if '.git' == url[len_url - 4: len_url]:
        url = url[:len_url - 4]

    import os
    path = os.path.join(repos_dir, url.split('/')[-1])

    import git
    if os.path.exists(path):
        repo = git.Repo(path)
    else:
        repo = git.Repo.clone_from(url, path, branch=branch)

    # blast any current changes
    repo.git.reset('--hard')

    # ensure master is checked out
    repo.heads[branch].checkout()
    # repo.heads.master.checkout()

    # blast any changes there (only if it wasn't checked out)
    repo.git.reset('--hard')

    # remove any extra non-tracked files (.pyc, etc)
    repo.git.clean('-xdf')

    # pull in the changes from from the remote
    repo.remotes.origin.pull()


if __name__ == '__main__':
    if PROXY:
        import os
        os.environ['http_proxy'] = PROXY

    from github import Github
    gh = Github(LOGIN, PASSWORD)

    # Пользователь, чьи репозитории собираемся импортировать
    user = 'gil9red'

    import os.path
    if not os.path.exists(REPOS_DIR):
        os.makedirs(REPOS_DIR)

    # Только публичные репозитории (форки и приватные репозитории игнорируются)
    for repo in filter(lambda repo: not repo.fork and not repo.private, gh.get_user(user).get_repos()):
        print(repo, repo.url)
        get_repo(repo.html_url, REPOS_DIR, repo.default_branch)
