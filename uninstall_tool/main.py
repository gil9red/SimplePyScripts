#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from winreg import *


UNINSTALL_PATH_LIST = [
    r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
    r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
]

programs_dict = dict()

for path in UNINSTALL_PATH_LIST:
    with OpenKey(HKEY_LOCAL_MACHINE, path) as key:
        for i in range(QueryInfoKey(key)[0]):
            keyname = EnumKey(key, i)
            subkey = OpenKey(key, keyname)

            try:
                subkey_dict = dict()
                for j in range(QueryInfoKey(subkey)[1]):
                    k, v = EnumValue(subkey, j)[:2]
                    subkey_dict[k] = v

                if 'DisplayName' not in subkey_dict:
                    continue

                name = subkey_dict['DisplayName'].strip()
                if not name:
                    continue

                programs_dict[name] = subkey_dict

            except WindowsError:
                pass


for number, name in enumerate(sorted(programs_dict.keys()), 1):
    subkey_dict = programs_dict[name]
    print('{}. {}:'.format(number, name))
    print('    {}: {}'.format('DisplayVersion', subkey_dict.get('DisplayVersion', '')))
    print()


# # import errno, os, winreg
# # proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
# # proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
# #
# # if proc_arch == 'x86' and not proc_arch64:
# #     arch_keys = {0}
# # elif proc_arch == 'x86' or proc_arch == 'amd64':
# #     arch_keys = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}
# # else:
# #     raise Exception("Unhandled arch: %s" % proc_arch)
# #
# # number = 1
# #
# # for arch_key in arch_keys:
# #     key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | arch_key)
# #     for i in range(0, winreg.QueryInfoKey(key)[0]):
# #         skey_name = winreg.EnumKey(key, i)
# #         skey = winreg.OpenKey(key, skey_name)
# #         try:
# #             print(number, winreg.QueryValueEx(skey, 'DisplayName')[0])
# #             number += 1
# #         except OSError as e:
# #             if e.errno == errno.ENOENT:
# #                 # DisplayName doesn't exist in this skey
# #                 pass
# #         finally:
# #             skey.Close()
#
#
# import errno, os, winreg
# proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
# proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
#
# if proc_arch == 'x86' and not proc_arch64:
#     arch_keys = {0}
# elif proc_arch == 'x86' or proc_arch == 'amd64':
#     arch_keys = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}
# else:
#     raise Exception("Unhandled arch: %s" % proc_arch)
#
# number = 1
# programs_dict = dict()
#
# for arch_key in arch_keys:
#     key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | arch_key)
#     for i in range(0, winreg.QueryInfoKey(key)[0]):
#         keyname = winreg.EnumKey(key, i)
#         subkey = winreg.OpenKey(key, keyname)
#
#         try:
#             subkey_dict = dict()
#             for j in range(winreg.QueryInfoKey(subkey)[1]):
#                 k, v = winreg.EnumValue(subkey, j)[:2]
#                 subkey_dict[k] = v
#
#             # if 'DisplayName' not in subkey_dict or 'UninstallString' not in subkey_dict:
#             #     continue
#             if 'DisplayName' not in subkey_dict:
#                 continue
#
#             name = subkey_dict['DisplayName'].strip()
#             if not name:
#                 continue
#
#             programs_dict[name] = subkey_dict
#
#         except WindowsError:
#             pass
#
#         # skey_name = winreg.EnumKey(key, i)
#         # skey = winreg.OpenKey(key, skey_name)
#         # try:
#         #     print(number, winreg.QueryValueEx(skey, 'DisplayName')[0])
#         #     number += 1
#         # except OSError as e:
#         #     if e.errno == errno.ENOENT:
#         #         # DisplayName doesn't exist in this skey
#         #         pass
#         # finally:
#         #     skey.Close()
#
#
#
# number = 1
# for name in sorted(programs_dict.keys()):
#     subkey_dict = programs_dict[name]
#     print('{}. {}:'.format(number, name), subkey_dict)
#     # print('    {}: {}'.format('UninstallString', subkey_dict['UninstallString']))
#     # print('    {}: {}'.format('DisplayIcon', subkey_dict.get('DisplayIcon', '')))
#     # print('    {}: {}'.format('DisplayVersion', subkey_dict.get('DisplayVersion', '')))
#     # print('    {}: {}'.format('Publisher', subkey_dict.get('Publisher', '')))
#     print()
#     number += 1
#
#
#
# quit()
#
# # https://gist.github.com/gil9red/245ad29bb6b4b2b99f4324a12bf538dd
#
# from winreg import *
#
# with OpenKey(HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall") as key:
#     programs_dict = dict()
#
#     for i in range(QueryInfoKey(key)[0]):
#         keyname = EnumKey(key, i)
#         subkey = OpenKey(key, keyname)
#
#         try:
#             subkey_dict = dict()
#             for j in range(QueryInfoKey(subkey)[1]):
#                 k, v = EnumValue(subkey, j)[:2]
#                 subkey_dict[k] = v
#
#             if 'DisplayName' not in subkey_dict or 'UninstallString' not in subkey_dict:
#                 continue
#
#             name = subkey_dict['DisplayName'].strip()
#             if not name:
#                 continue
#
#             programs_dict[name] = subkey_dict
#
#         except WindowsError:
#             pass
#
#     number = 1
#     for name in sorted(programs_dict.keys()):
#         subkey_dict = programs_dict[name]
#         print('{}. {}:'.format(number, name))
#         print('    {}: {}'.format('UninstallString', subkey_dict['UninstallString']))
#         print('    {}: {}'.format('DisplayIcon', subkey_dict.get('DisplayIcon', '')))
#         print('    {}: {}'.format('DisplayVersion', subkey_dict.get('DisplayVersion', '')))
#         print('    {}: {}'.format('Publisher', subkey_dict.get('Publisher', '')))
#         print()
#         number += 1
