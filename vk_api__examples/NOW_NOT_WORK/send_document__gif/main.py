#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from pathlib import Path

from vk_api.upload import VkUpload

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent.parent
sys.path.append(str(ROOT_DIR))
from root_common import get_vk_session


def upload_doc(upload: VkUpload, file_name: str) -> str:
    rs = upload.document(file_name)
    doc = rs['doc']

    # Составление названия документа: https://vk.com/dev/messages.send
    return f"doc{doc['owner_id']}_{doc['id']}"


USER_ID = None

vk_session = get_vk_session()
upload = VkUpload(vk_session)

file_name = 'file_name.gif'

attachment = upload_doc(upload, file_name)
print('https://vk.com/' + attachment)

vk_session.method('messages.send', {
    'user_id': USER_ID,
    'attachment': attachment,
})
