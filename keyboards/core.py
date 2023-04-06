from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_remove = types.ReplyKeyboardRemove()

kb_start = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_start.add(
    KeyboardButton('/start'), KeyboardButton('/number'), 
    KeyboardButton('/addnumber'), KeyboardButton('/убратькнопки')
)

kb_stop_fsm = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_stop_fsm.add(KeyboardButton('/stop'))
