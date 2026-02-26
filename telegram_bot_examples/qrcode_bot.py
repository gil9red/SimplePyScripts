#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from io import BytesIO

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext

# pip install qrcode
import qrcode

from common import get_logger, log_func, start_bot, run_main


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, _: CallbackContext) -> None:
    update.effective_message.reply_text("Write something")


@log_func(log)
def on_request(update: Update, _: CallbackContext) -> None:
    message = update.effective_message

    bytes_io = BytesIO()

    img = qrcode.make(message.text)
    img.save(bytes_io, format="PNG")

    # После выполнения save внутренний указатель будет в конце данных,
    # а для работы с bytes_io нужно вернуть в начало
    bytes_io.seek(0)

    message.reply_photo(photo=bytes_io, quote=True)


def main() -> None:
    handlers = [
        CommandHandler("start", on_start),
        MessageHandler(Filters.text, on_request),
    ]
    start_bot(log, handlers)


if __name__ == "__main__":
    run_main(main, log)
