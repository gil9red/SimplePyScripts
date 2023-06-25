#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

import youtube_dl


def download_youtube(url):
    with youtube_dl.YoutubeDL() as ydl:
        try:
            retcode = ydl.download([url])
        except youtube_dl.MaxDownloadsReached:
            ydl.to_screen("--max-download limit reached, aborting.")
            retcode = 101

    return retcode


url = "bupTAbtQYic"
code = download_youtube(url)
sys.exit(code)


# youtube_dl.main(['--help'])
# youtube_dl.main(['bupTAbtQYic'])

# from youtube_dl.extractor import YoutubeIE
#
# ie = YoutubeIE()
#
# @staticmethod
# def add_extra_info(info_dict, extra_info):
#     '''Set the keys from extra_info in info dict if they are missing'''
#     for key, value in extra_info.items():
#         info_dict.setdefault(key, value)
#
# def add_default_extra_info(self, ie_result, ie, url):
#     self.add_extra_info(ie_result, {
#         'extractor': ie.IE_NAME,
#         'webpage_url': url,
#         'webpage_url_basename': url_basename(url),
#         'extractor_key': ie.ie_key(),
#     })
#
# try:
#     ie_result = ie.extract(url)
#     if ie_result is None:  # Finished already (backwards compatibility; listformats and friends should be moved here)
#         break
#     if isinstance(ie_result, list):
#         # Backwards compatibility: old IE result format
#         ie_result = {
#             '_type': 'compat_list',
#             'entries': ie_result,
#         }
#     self.add_default_extra_info(ie_result, ie, url)
#     if process:
#         return self.process_ie_result(ie_result, download, extra_info)
#     else:
#         return ie_result
# except ExtractorError as de:  # An error we somewhat expected
#     self.report_error(compat_str(de), de.format_traceback())
#     break
# except MaxDownloadsReached:
#     raise
# except Exception as e:
#     if self.params.get('ignoreerrors', False):
#         self.report_error(compat_str(e), tb=compat_str(traceback.format_exc()))
#         break
#     else:
#         raise
