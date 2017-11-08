#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import svn.local
repo = svn.local.LocalClient('E:/OPTT/optt_trunk')

# OR:
# import svn.remote
# repo = svn.remote.RemoteClient('svn+cplus://svn2.compassplus.ru/twrbs/csm/optt/dev/trunk')


log_list = [log for log in repo.log_default()]
print('Total commits:', len(log_list))
print()

release_version_log_list = [log for log in log_list if log.msg and 'Release version' in log.msg]
print('Release version log ({}):'.format(len(release_version_log_list)))

for i, log in enumerate(release_version_log_list, 1):
    print('    {:6}. [rev {}] {} {:15} "{}"'.format(i, log.revision, log.date, log.author, log.msg))
