from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.core import kb_start, kb_stop_fsm
from keyboards.get_number import kb_inline
from models.utils.numbers import get_numbers
from service.settings import bot, cd_search


class FSMSearch(StatesGroup):
    value = State()


async def get_numbers_from_fio(message: types.Message):
    """
    Запрос на поиск по одному из полей в моделе
    """
    await bot.send_message(
        message.chat.id, 
        'По какому полю поиск?\n\n',
        reply_markup=kb_inline,
    )


async def callback_search_number(call: types.CallbackQuery, callback_data: dict):
    """
    Сохраняет action и ждет ключевое слово для поиска
    """
    global action
    action = callback_data.get('action')
    await FSMSearch.value.set()
    await call.bot.send_message(
        call.message.chat.id, 
        'Что ищем?',
        reply_markup=kb_stop_fsm,
    )


async def value_from_fio(message: types.Message, state: FSMContext):
    """
    Записывает ключевое слово и выдает результат если он есть
    """
    async with state.proxy() as data:
        data['value'] = message.text
        response = get_numbers(action, data['value'])
        if response:
            await bot.send_message(
                message.chat.id, 
                response,
                reply_markup=kb_start,
            )
        else:
            await bot.send_message(
                message.chat.id, 
                'Записи не найдены или произошла ошибка, '
                'проверьте введенные данные',
                reply_markup=kb_start,
            )
            
    await state.finish()


def register_handlers_search_number(dp: Dispatcher):
    dp.register_message_handler(get_numbers_from_fio, commands=['number'], state=None)
    dp.register_callback_query_handler(callback_search_number, cd_search.filter(), state=None)
    dp.register_message_handler(value_from_fio, state=FSMSearch.value)
