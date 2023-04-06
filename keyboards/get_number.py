from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from service.settings import cd_search

kb_get = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_get.add(
    KeyboardButton('last_name'), KeyboardButton('first_name'), 
    KeyboardButton('patronymic'), KeyboardButton('/stop')
)


kb_inline = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton('Фамилия', callback_data=cd_search.new(
        action='last_name',
    )),
    InlineKeyboardButton('Имя', callback_data=cd_search.new(
        action='first_name',
    )),
    InlineKeyboardButton('Отчество', callback_data=cd_search.new(
        action='patronymic',
    )),
)
