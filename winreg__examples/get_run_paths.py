#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.windxp.com.ru/autrun.htm
# SOURCE: http://www.infosecurity.ru/_gazeta/content/090904/art3.shtml
# SOURCE: https://www.saule-spb.ru/library/autorun.html


from typing import Dict, List

from common import get_key, get_entry, Entry, get_entries


PATHS = [
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run",

    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce",

    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",

    # TODO: оставить?
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",

    # TODO: оставить?
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices",

    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce",

    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup",

    r"HKEY_CURRENT_USER\Software\Microsoft\WindowsNT\CurrentVersion\Windows\load",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\WindowsNT\CurrentVersion\Winlogon\Userinit",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnceEx",
]





# SOURCE: https://www.microsoftpressstore.com/articles/article.aspx?p=2762082&seqNum=2
r"""
# Per-user ASEPs under HKCU\Software
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Runonce
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\RunonceEx
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Windows\Load
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Windows\Run
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell

# Per-user ASEPs under HKCU\Software—64-bit only
HKCU\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce

# Per-user ASEPs under HKCU\Software intended to be controlled through Group Policy
HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System\Shell
HKCU\Software\Policies\Microsoft\Windows\System\Scripts\Logon
HKCU\Software\Policies\Microsoft\Windows\System\Scripts\Logoff

# Systemwide ASEPs in the registry
HKLM\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnceEx
HKLM\Software\Microsoft\Active Setup\Installed Components
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Runonce
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\RunonceEx
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\IconServiceLib
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\AlternateShells\AvailableShells
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\AppSetup
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Taskman
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\VmApplet
HKLM\System\CurrentControlSet\Control\SafeBoot\AlternateShell
HKLM\System\CurrentControlSet\Control\Terminal Server\Wds\rdpwd\StartupPrograms
HKLM\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp\InitialProgram

# Systemwide ASEPs in the registry, intended to be controlled through Group Policy
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System\Shell
HKLM\Software\Policies\Microsoft\Windows\System\Scripts\Logon
HKLM\Software\Policies\Microsoft\Windows\System\Scripts\Logoff
HKLM\Software\Policies\Microsoft\Windows\System\Scripts\Startup
HKLM\Software\Policies\Microsoft\Windows\System\Scripts\Shutdown
HKLM\Software\Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Startup
HKLM\Software\Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Shutdown

# Systemwide ASEPs in the registry—64-bit only
HKLM\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce
HKLM\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx
HKLM\Software\Wow6432Node\Microsoft\Active Setup\Installed Components

# Systemwide ActiveSync ASEPs in the registry
HKLM\Software\Microsoft\Windows CE Services\AutoStartOnConnect
HKLM\Software\Microsoft\Windows CE Services\AutoStartOnDisconnect

# Systemwide ActiveSync ASEPs in the registry—64-bit only
HKLM\Software\Wow6432Node\Microsoft\Windows CE Services\AutoStartOnConnect
HKLM\Software\Wow6432Node\Microsoft\Windows CE Services\AutoStartOnDisconnect
"""





# TODO: не использовать, пусть такие пути описываются как кортеж, где вторым элементом будет имя значения
# def get_value_for_full_path(path_with_value: str, expand_vars=True) -> Optional[Entry]:
#     path, value = path_with_value.split(', ')
#     return get_value(path, value, expand_vars)


for path, value in [
    # r'HKCU\Software\Microsoft\Windows NT\CurrentVersion\Windows, Load',
    # r'HKCU\Software\Microsoft\Windows NT\CurrentVersion\Windows, Run',
    # r'HKCU\Software\Microsoft\Windows NT\CurrentVersion\Windows, Shell',
    # r'HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer, Run',
    # r'HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer, Shell',
    # r'HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer, Run',
    # r'HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer, Shell',

    (r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 'Common Startup'),
    (r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 'Common AltStartup'),
    (r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders', 'Common Startup'),
    (r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders', 'Common AltStartup'),

    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 'Startup'),
    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 'AltStartup'),
    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders', 'Startup'),
    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders', 'AltStartup'),
]:
    print(f'{path}/{value} =', get_entry(path, value))

quit()

# path = r'HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon'
# print(get_values(path))
# print(get_values(path + r'\123'))
# print(get_value(path, 'Shell'))
# print(get_value(path, 'Shell123'))
#
# path_with_value = r'HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon, Shell'
# print(get_value_for_full_path(path_with_value))
# print()


def get_run_paths(expand_vars=True) -> Dict[str, List[Entry]]:
    path_by_entries = dict()

    for path in PATHS:
        key = get_key(path)
        if not key:
            continue

        path_by_entries[path] = get_entries(path, expand_vars)

    return path_by_entries


if __name__ == '__main__':
    run_paths = get_run_paths()
    for path, entries in run_paths.items():
        print(path)

        for i, entry in enumerate(entries, 1):
            print(f'    {i}. {entry.name}: {entry.value}')

        print()
    r"""
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
        1. Lync: "C:\Program Files (x86)\Microsoft Office\Office15\lync.exe" /fromrunkey
        2. Zoom: "C:\Users\IPetrash\AppData\Roaming\Zoom\bin\Zoom.exe"
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
        1. RTHDVCPL: "C:\Program Files\Realtek\Audio\HDA\RtkNGUI64.exe" -s
        2. DocFetcher-Daemon: C:\Program Files (x86)\DocFetcher\docfetcher-daemon-windows.exe
        3. egui: "C:\Program Files\ESET\ESET Security\ecmds.exe" /run /hide /proxy
        4. SecurityHealth: C:\Program Files\Windows Defender\MSASCuiL.exe
    
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce
    
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
    
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
    
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices
    
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup

    """