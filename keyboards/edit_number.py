from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from service.settings import cd_edit


def edit_number_inline(response_id):
    kb_inline = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton('Фамилию', callback_data=cd_edit.new(
            action='last_name',
            num_id=response_id,
        )),
        InlineKeyboardButton('Имя', callback_data=cd_edit.new(
            action='first_name',
            num_id=response_id,
        )),
        InlineKeyboardButton('Отчество', callback_data=cd_edit.new(
            action='patronymic',
            num_id=response_id,
        )),
        InlineKeyboardButton('Номер', callback_data=cd_edit.new(
            action='number',
            num_id=response_id,
        )),
        InlineKeyboardButton('Удалить', callback_data=cd_edit.new(
            action='delete',
            num_id=response_id,
        )),
    )

    return kb_inline
