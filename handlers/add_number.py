from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.core import kb_remove, kb_start, kb_stop_fsm
from models.utils.numbers import set_number
from service.settings import bot, whitelist


class FSMNewNumber(StatesGroup):
    last_name = State()
    first_name = State()
    patronymic = State()
    number = State()


async def add_number(message: types.Message):
    """
    Добавить новую запись в модель, ждет фамилию
    """
    if not str(message.from_user.id) in whitelist:
        await FSMNewNumber.last_name.set()
        await bot.send_message(
            message.chat.id, 
            'Введите фамилию',
            reply_markup=kb_stop_fsm,
        )
    else:
        await bot.send_message(
            message.chat.id, 
            'Нет доступа', 
            reply_markup=kb_start,
        )


async def last_name_add_number(message: types.Message, state: FSMContext):
    """
    Записывает фамилию и ждет имя
    """
    async with state.proxy() as data:
        data['last_name'] = message.text
        await FSMNewNumber.next()
        await bot.send_message(
            message.chat.id, 
            'Введите имя', 
            reply_markup=kb_remove,
        )     


async def first_name_add_number(message: types.Message, state: FSMContext):
    """
    Записывает имя и ждет отчество
    """
    async with state.proxy() as data:
        data['first_name'] = message.text
        await FSMNewNumber.next()
        await bot.send_message(
            message.chat.id, 
            'Введите отчество', 
            reply_markup=kb_remove,
        )   
        
        
async def patronymic_add_number(message: types.Message, state: FSMContext):
    """
    Записывает отчество и ждет номер
    """
    async with state.proxy() as data:
        data['patronymic'] = message.text
        await FSMNewNumber.next()
        await bot.send_message(
            message.chat.id, 
            'Введите номер', 
            reply_markup=kb_remove,
        )   
      
  
async def number_add_number(message: types.Message, state: FSMContext):
    """
    Записывает номер и закрывает машину состояний, создает запись в моделе
    """
    async with state.proxy() as data:
        data['number'] = message.text
        result = set_number(
            message.from_user, 
            data,
        )
        if result:
            await bot.send_message(
                message.chat.id, 
                'Данные внесены',
                reply_markup=kb_start,
            )
        else:
            await bot.send_message(
                message.chat.id, 
                'Команда использована неверно',
                reply_markup=kb_start,
            )
        
    await state.finish()   
    

def register_handlers_add_number(dp: Dispatcher):
    dp.register_message_handler(add_number, commands=['addnumber'], state=None)
    dp.register_message_handler(last_name_add_number, state=FSMNewNumber.last_name)
    dp.register_message_handler(first_name_add_number, state=FSMNewNumber.first_name)
    dp.register_message_handler(patronymic_add_number, state=FSMNewNumber.patronymic)
    dp.register_message_handler(number_add_number, state=FSMNewNumber.number)
