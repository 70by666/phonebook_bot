from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.core import kb_start, kb_stop_fsm
from keyboards.edit_number import edit_number_inline
from models.utils.numbers import edit_number, get_number
from service.settings import bot, cd_edit, whitelist


class FSMEdit(StatesGroup):
    value = State()
    

async def get_number_from_id(message: types.Message):
    """
    Получить запись по id
    """
    if not str(message.from_user.id) in whitelist:
        try:
            response = get_number(message.text.split(' ')[1])
            if response:
                kb_inline = edit_number_inline(response.id)
                text_message = '{} {} {} {} {}\n\nИзменить:'.format(
                    response.id,
                    response.last_name,
                    response.first_name,
                    response.patronymic,
                    response.number,
                )
                await bot.send_message(
                    message.chat.id, 
                    text_message,
                    reply_markup=kb_inline,
                )
            else:
                await bot.send_message(
                    message.chat.id, 
                    'Запись с таким ID не найдена',
                    reply_markup=kb_start,
                )
        except IndexError:
            await bot.send_message(
                message.chat.id, 
                'Вы не указали ID',
                reply_markup=kb_start,
            )
    else:
        await bot.send_message(
            message.chat.id, 
            'Нет доступа', 
            reply_markup=kb_start,
        )


async def callback_edit_number(call: types.CallbackQuery, callback_data: dict):
    """
    Изменить/удалить запись
    """
    global action
    global num_id
    action = callback_data.get('action')
    num_id = callback_data.get('num_id')
    if not action == 'delete':
        await FSMEdit.value.set()
        await call.bot.send_message(
            call.message.chat.id, 
            'Введите новое значение',
            reply_markup=kb_stop_fsm,
        )
    else:
        result = edit_number(action, num_id)
        if result:
            await bot.send_message(
                call.message.chat.id, 
                f'Номер удален',
                reply_markup=kb_start,
            )
        else:
            await bot.send_message(
                call.message.chat.id, 
                'Команда использована неверно',
                reply_markup=kb_start,
            )
    

async def edit_value(message: types.Message, state: FSMContext):
    """
    Записывается значение и изменяется запись
    """
    async with state.proxy() as data:
        data['value'] = message.text
        result = edit_number(action, num_id, data['value'])
        if result:
            await bot.send_message(
                message.chat.id, 
                f'Данные изменены',
                reply_markup=kb_start,
            )
        else:
            await bot.send_message(
                message.chat.id, 
                'Команда использована неверно',
                reply_markup=kb_start,
            )
        
    await state.finish()
    
    
def register_handlers_edit_number(dp: Dispatcher):
    dp.register_message_handler(get_number_from_id, commands=['getnumber'])
    dp.register_callback_query_handler(callback_edit_number, cd_edit.filter(), state=None)
    dp.register_message_handler(edit_value, state=FSMEdit.value)
